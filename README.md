# Sentry BigQuery plugin

Plugin for Sentry which forward data to [BigQuery](https://cloud.google.com/bigquery).


## Installation


1. Install this package

```bash
pip install sentry-bigquery
```
2. Restart your Sentry instance.
3. Go to your Sentry web interface. Open ``Settings`` page of one of your projects.
4. On ``Integrations`` (or ``Legacy Integrations``) page, find ``BigQuery`` plugin and enable it.
5. Configure plugin on ``Configure plugin`` page.
 - Add project ID (Dataset ID from admin panel)
 - Add [account info](https://cloud.google.com/iam/docs/creating-managing-service-account-keys) file
6. Done!
