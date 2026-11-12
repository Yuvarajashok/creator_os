# User workflow and data handling

[Back to README](../README.md)

These steps describe the intended interface after setup blockers are resolved, not a tested hosted service.

1. Register an account or use the synthetic demo account in an isolated development instance.
2. Add a page record using its Instagram username and optional biography.
3. Add or review post metrics through the interface/API.
4. Open the dashboard for the selected page and analysis period.
5. Read signal breakdowns and recommendations together with the available-data count.

Adding a page record does not connect an Instagram account. There is no completed OAuth onboarding/live-data sync in this source.

## Interpreting scores

Overall score combines seven weighted signals. Growth-stage labels and recommendations are program rules. Confidence measures data completeness/quality, not a probability that recommendations will work. A low-data fallback must not be presented as a reliable growth forecast.

The predictor uses existing engagement metrics. No validated pre-publication virality claim is supported.

## Data and backups

The database contains accounts, pages, posts, metrics, and scores. JWT tokens are held in browser localStorage. Generated model/scaler files are separate from database storage.

No complete user-facing backup/restore workflow is documented as implemented. For development, stop writers and back up the database/model storage privately using the chosen storage system's procedure; validate restores in a separate database.

Do not upload real account information, database dumps, screenshots containing personal data, secrets, or model artifacts to an issue or repository. Use synthetic examples.

## Demonstrations

The seed script uses fabricated metrics and a publicly documented demo password. Keep those records separate from real analytics. The scheduler's mock sync also fabricates metrics; running it against genuine records changes them.

Screenshots should be taken from a working local instance with synthetic data. None are supplied by this source-only documentation update.
