# Data Sources Setup Guide

This guide provides step-by-step instructions for setting up the data source integrations used by SEO Machine: Vercel Web Analytics (CSV-based), Google Search Console, DataForSEO, and WordPress.

---

## Table of Contents

1. [Vercel Web Analytics Setup](#vercel-web-analytics-setup)
2. [Google Search Console Setup](#google-search-console-setup)
3. [DataForSEO Setup](#dataforseo-setup)
4. [WordPress Setup](#wordpress-setup)
5. [Testing Your Integrations](#testing-your-integrations)
6. [Troubleshooting](#troubleshooting)

---

## Vercel Web Analytics Setup

Vercel Web Analytics provides traffic data and referrer breakdowns for your site. The integration reads CSVs you export from the Vercel dashboard — no API credentials needed.

### Prerequisites
- A Vercel project with Web Analytics enabled

### Step 1: Export the "Top Pages" CSVs

1. Open your project in the [Vercel dashboard](https://vercel.com/dashboard)
2. Click **Analytics** → **Pages**
3. Use the date-range picker and **Export CSV** to download four files, one per window:
   - **Last 24 hours**
   - **Last 7 days**
   - **Last 30 days**
   - **Last 90 days**
4. Keep Vercel's default filenames (e.g. `Top Pages - Mar 4, 13_00 - Jun 4, 14_59.csv`). The loader parses the dates from the filename to bucket each export to a window.

### Step 2: Export the "Top Referrers" CSV

1. In the same Analytics view, click **Referrers**
2. Set the range to **Last 90 days** and **Export CSV**
3. Save the file with its default name (e.g. `Top Referrers - Mar 4, 13_00 - Jun 4, 14_59.csv`)

### Step 3: Place the CSVs

Drop all five CSVs at the repo root. If you'd rather keep them elsewhere, set:
```
VERCEL_ANALYTICS_DIR=/absolute/path/to/your/csv/folder
```
in your `.env` file.

### Step 4: Refresh Periodically

Whenever you want fresh data, re-export the CSVs from Vercel and overwrite (or just add — the loader picks the most recently modified file per window). A weekly cadence is usually enough for SEO content workflows.

### Limitations

CSV exports do not include conversion events, bounce rate, engagement time, or per-page traffic sources. For those, you'd need to set up [Vercel Drains](https://vercel.com/docs/drains/reference/analytics) streaming events to your own datastore.

---

## Google Search Console Setup

Google Search Console provides search query data, click-through rates, average positions, and impressions for your website in Google Search results.

### Prerequisites
- Verified ownership of your website in Google Search Console
- A Google Cloud project

### Step 1: Enable the Google Search Console API

1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
2. Select or create a project
3. Navigate to **APIs & Services > Library**
4. Search for "Google Search Console API"
5. Click on the API and click **Enable**

### Step 2: Create a Service Account

1. In Google Cloud Console, go to **APIs & Services > Credentials**
2. Click **Create Credentials** and select **Service Account**
3. Fill in the service account details:
   - **Name**: `seo-machine-gsc` (or any descriptive name)
   - **Description**: "Service account for SEO Machine GSC integration"
4. Click **Create and Continue**, then skip the optional steps and click **Done**
5. Find the service account in the **Credentials** page, click its email, go to the **Keys** tab
6. Click **Add Key > Create new key**, choose **JSON**, click **Create**. The key file downloads automatically.

### Step 3: Grant Access to Your Search Console Property

1. Go to [Google Search Console](https://search.google.com/search-console)
2. Select your property (website)
3. Click **Settings** in the left sidebar
4. Click **Users and permissions** → **Add user**
5. Enter the service account email (e.g., `seo-machine-gsc@your-project.iam.gserviceaccount.com`)
6. Select permission level: **Full** (required for API access, but only provides read access)
7. Click **Add**

### Step 4: Get Your Site URL

Your site URL is the property name in Search Console, typically one of:
- `https://yoursite.com/` (for URL prefix properties)
- `sc-domain:yoursite.com` (for domain properties)
- Check in Search Console settings to confirm the exact format

### Step 5: Configure the Integration

1. Rename the JSON key to `gsc-credentials.json`
2. Move to: `credentials/gsc-credentials.json`
3. Add to your `.env` file:
   ```
   GSC_SITE_URL=https://yoursite.com/
   GSC_CREDENTIALS_PATH=credentials/gsc-credentials.json
   ```

---

## DataForSEO Setup

DataForSEO provides keyword research data, search volume, competition metrics, and SERP analysis.

### Prerequisites
- A DataForSEO account
- API credits (free trial available, or paid plan)

### Step 1: Create a DataForSEO Account

1. Go to [DataForSEO](https://dataforseo.com/)
2. Click **Sign Up** or **Get Started**
3. Complete the registration process
4. Verify your email address

### Step 2: Get Your API Credentials

1. Log in to your DataForSEO account
2. Go to the [Dashboard](https://app.dataforseo.com/)
3. Navigate to **API Access** or **API Credentials**
4. You'll see your:
   - **Login** (username/email)
   - **Password** (API password, different from account password)
5. Copy both values

**Note**: DataForSEO uses Basic Authentication with login/password, not API keys.

### Step 3: Add Credits to Your Account

1. In the DataForSEO dashboard, go to **Billing** or **Add Credits**
2. Choose a payment option:
   - **Free Trial**: Usually provides $1-5 in credits to test
   - **Pay As You Go**: Add credits as needed
   - **Monthly Plan**: Subscribe for discounted rates
3. Complete the payment process

### Step 4: Configure the Integration

Add the following to your `.env` file:
```
DATAFORSEO_LOGIN=your_username_or_email
DATAFORSEO_PASSWORD=your_api_password
```

### API Usage and Costs

DataForSEO charges per API request. Common pricing:
- **Keywords For Site**: ~$0.10 per 1000 keywords
- **Search Volume**: ~$0.20 per 1000 keywords
- **SERP Analysis**: ~$0.005 per SERP

**Tip**: Start with the free trial to test the integration, then add credits based on your usage needs.

---

## WordPress Setup

WordPress integration enables publishing articles and landing pages directly from SEO Machine via the REST API.

### Prerequisites
- A WordPress site with REST API enabled
- Admin access to install plugins
- Yoast SEO plugin installed (for SEO metadata)

### Step 1: Install the MU-Plugin

1. Copy `wordpress/seo-machine-yoast-rest.php` to your WordPress site's `wp-content/mu-plugins/` directory
2. This plugin exposes Yoast SEO fields via the REST API for programmatic publishing

### Step 2: Create an Application Password

1. Log in to your WordPress admin
2. Go to **Users > Profile**
3. Scroll to **Application Passwords**
4. Enter a name: `SEO Machine`
5. Click **Add New Application Password**
6. Copy the generated password (you won't see it again)

### Step 3: Configure the Integration

Add the following to your `.env` file:
```
WP_URL=https://yoursite.com
WP_USERNAME=your_admin_username
WP_APP_PASSWORD=xxxx xxxx xxxx xxxx xxxx xxxx
```

### Step 4: Optional Theme Integration

Add the snippet from `wordpress/functions-snippet.php` to your theme's `functions.php` for additional publishing features.

See `wordpress/README.md` for more details.

---

## Testing Your Integrations

After setting up your data sources, test them to ensure they're working correctly.

### Test Vercel Analytics Integration

With the CSVs at the repo root, run the module directly:
```bash
python3 data_sources/modules/vercel_analytics.py
```

Expected output:
- A list of detected windows (e.g. `[1, 7, 30, 90] day(s)`)
- Top 10 pages from the 30-day window
- Top traffic sources (from the Top Referrers CSV)

### Test Google Search Console Integration

Run the GSC agent to fetch search data:
```bash
npm run agent:gsc-search-data
```

Expected output:
- List of top search queries
- Click and impression data
- Average position metrics

### Test DataForSEO Integration

Run the keyword research agent:
```bash
npm run agent:keyword-research "your target keyword"
```

Expected output:
- Keyword suggestions related to your query
- Search volume data
- Keyword difficulty scores

---

## Troubleshooting

### Vercel Analytics Issues

**Error: "No 'Top Pages*.csv' exports found in ..."**
- Make sure the CSVs are at the repo root (or wherever `VERCEL_ANALYTICS_DIR` points)
- Filenames must match Vercel's default format: `Top Pages - <Mon DD>, <HH_MM> - <Mon DD>, <HH_MM>.csv`

**Only one or two windows detected**
- Export all four windows from the Vercel dashboard (24h / 7d / 30d / 90d)
- Trend analysis needs at least two windows; declining-pages analysis needs two distinct window lengths

**Data feels stale**
- Re-export the CSVs from the dashboard and replace the files. The loader picks the most-recently-modified file per window.

### Google Search Console Issues

**Error: "User does not have sufficient permissions"**
- Verify the service account is added to Search Console with Full permissions
- Make sure you're using the correct site URL format in `.env`

**Error: "Site not found"**
- Check the `GSC_SITE_URL` format matches exactly what's in Search Console
- Try both formats: `https://yoursite.com/` and `sc-domain:yoursite.com`

### DataForSEO Issues

**Error: "Authentication failed"**
- Verify your login/password in `.env` are correct
- Make sure you're using the API password, not your account password
- Check for any extra spaces in the credentials

**Error: "Insufficient credits"**
- Check your account balance at app.dataforseo.com
- Add more credits or upgrade your plan

**Error: "Rate limit exceeded"**
- DataForSEO has rate limits; wait a few minutes before retrying
- Consider spreading out API calls over time

### General Issues

**Environment Variables Not Loading**
- Make sure your `.env` file is in the root directory
- Verify there are no syntax errors in the `.env` file
- Restart your application after modifying `.env`

**Credentials File Not Found**
- Check the file path is correct: `credentials/`
- Create the `credentials/` directory if it doesn't exist:
  ```bash
  mkdir -p credentials/
  ```
- Verify file names match exactly (case-sensitive)

---

## Security Best Practices

### Protect Your Credentials

1. **Never commit credentials to Git**
   - Add to `.gitignore`:
     ```
     credentials/
     .env
     ```

2. **Restrict file permissions**:
   ```bash
   chmod 600 credentials/*.json
   chmod 600 .env
   ```

3. **Rotate credentials regularly**
   - Regenerate service account keys every 90 days
   - Update DataForSEO password periodically

4. **Use principle of least privilege**
   - Only grant Viewer/Read access where possible
   - Don't share credentials between projects unnecessarily

### Backup Your Credentials

Store encrypted backups of your credentials in a secure location:
- Password manager (1Password, LastPass, etc.)
- Encrypted cloud storage
- Secure company vault

---

## Quick Reference

### File Structure
```
seomachine/
├── .env                          # Environment variables
├── credentials/
│   └── gsc-credentials.json     # GSC service account key
├── Top Pages*.csv                # Vercel Web Analytics exports (4 windows)
├── Top Referrers*.csv            # Vercel referrers export
├── config/
│   └── competitors.json         # Competitor configuration
└── data-sources-setup.md        # This file
```

### Environment Variables
```bash
# Vercel Analytics (optional — defaults to repo root)
# VERCEL_ANALYTICS_DIR=/path/to/csv/folder

# Google Search Console
GSC_SITE_URL=https://yoursite.com/
GSC_CREDENTIALS_PATH=credentials/gsc-credentials.json
COMPANY_NAME=Your Company

# DataForSEO
DATAFORSEO_LOGIN=your_username
DATAFORSEO_PASSWORD=your_api_password

# WordPress (optional, for /publish-draft)
WP_URL=https://yoursite.com
WP_USERNAME=your_username
WP_APP_PASSWORD=your_application_password
```

### Useful Links
- [Vercel Dashboard](https://vercel.com/dashboard)
- [Vercel Web Analytics docs](https://vercel.com/docs/analytics)
- [Google Cloud Console](https://console.cloud.google.com/)
- [Google Search Console](https://search.google.com/search-console)
- [DataForSEO Dashboard](https://app.dataforseo.com/)
- [DataForSEO API Documentation](https://docs.dataforseo.com/)

---

## Need Help?

If you encounter issues not covered in this guide:

1. Check the official documentation for each service
2. Review error logs for specific error messages
3. Verify all prerequisites are met
4. Test each integration independently to isolate the issue

---

**Last Updated**: January 2025
