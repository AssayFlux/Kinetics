"""Train independent XGBoost regressors for log10(Km) and log10(kcat)."""
from __future__ import annotations

import argparse
import json
import logging
from pathlib import Path

import joblib
import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import KFold, cross_val_score

LOG = logging.getLogger("kinetics.train")
TARGETS = ("log10_km", "log10_kcat")


def _load_npz(path: str | Path) -> tuple[np.ndarray, np.ndarray]:
    with np.load(path, allow_pickle=False) as data:
        X, y = data["X"].astype(np.float32), data["y"].astype(np.float32)
    if X.ndim != 2 or y.ndim != 2 or y.shape[1] != 2 or len(X) != len(y):
        raise ValueError(f"Expected X=(n, features), y=(n, 2); got {X.shape}, {y.shape}")
    if len(X) < 5:
        raise ValueError("At least five training samples are required for 5-fold CV.")
    if not np.isfinite(X).all() or not np.isfinite(y).all():
        raise ValueError("Features/targets contain NaN or infinite values.")
    return X, y


def train(train_npz: str | Path, test_npz: str | Path, model_dir: str | Path = "models",
          seed: int = 42, n_estimators: int = 500, max_depth: int = 6) -> dict:
    try:
        from xgboost import XGBRegressor
    except ImportError as exc:
        raise RuntimeError("Training requires xgboost. Install requirements.txt.") from exc
    X_train, y_train = _load_npz(train_npz)
    with np.load(test_npz, allow_pickle=False) as test:
        X_test, y_test = test["X"].astype(np.float32), test["y"].astype(np.float32)
    if X_test.ndim != 2 or X_test.shape[1] != X_train.shape[1] or y_test.shape != (len(X_test), 2):
        raise ValueError("Test feature/target shapes do not match the training data.")
    if len(X_test) == 0 or not np.isfinite(X_test).all() or not np.isfinite(y_test).all():
        raise ValueError("Test data is empty or contains non-finite values.")

    out = Path(model_dir)
    out.mkdir(parents=True, exist_ok=True)
    cv = KFold(n_splits=5, shuffle=True, random_state=seed)
    bundle = {"models": {}, "feature_dim": int(X_train.shape[1]), "targets": list(TARGETS),
              "esm_model": "facebook/esm2_t6_8M_UR50D", "fingerprint_bits": 2048, "radius": 2}
    report = {"cross_validation": {}, "test": {}}
    for i, target in enumerate(TARGETS):
        estimator = XGBRegressor(
            n_estimators=n_estimators, max_depth=max_depth, learning_rate=0.05,
            subsample=0.85, colsample_bytree=0.85, objective="reg:squarederror",
            n_jobs=-1, random_state=seed, tree_method="hist",
        )
        cv_rmse = -cross_val_score(
            estimator, X_train, y_train[:, i], cv=cv,
            scoring="neg_root_mean_squared_error", n_jobs=1,
        )
        estimator.fit(X_train, y_train[:, i])
        pred = estimator.predict(X_test)
        report["cross_validation"][target] = {
            "rmse_mean": float(cv_rmse.mean()), "rmse_std": float(cv_rmse.std()),
            "fold_rmse": cv_rmse.tolist(),
        }
        report["test"][target] = {
            "r2": float(r2_score(y_test[:, i], pred)),
            "rmse": float(np.sqrt(mean_squared_error(y_test[:, i], pred))),
            "mae": float(mean_absolute_error(y_test[:, i], pred)),
        }
        bundle["models"][target] = estimator
        estimator.save_model(out / f"{target}.json")
        LOG.info("%s: CV RMSE %.4f ± %.4f | test R2 %.4f RMSE %.4f MAE %.4f",
                 target, cv_rmse.mean(), cv_rmse.std(), report["test"][target]["r2"],
                 report["test"][target]["rmse"], report["test"][target]["mae"])
    joblib.dump(bundle, out / "kinetics_model.joblib", compress=3)
    (out / "metrics.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    LOG.info("Saved model bundle and metrics to %s", out)
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--train", default="data/train_features.npz")
    parser.add_argument("--test", default="data/test_features.npz")
    parser.add_argument("--model-dir", default="models")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--estimators", type=int, default=500)
    parser.add_argument("--max-depth", type=int, default=6)
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    train(args.train, args.test, args.model_dir, args.seed, args.estimators, args.max_depth)


if __name__ == "__main__":
    main()
