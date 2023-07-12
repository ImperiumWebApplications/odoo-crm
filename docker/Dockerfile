FROM odoo:16.0
MAINTAINER admin@leadquelle.net
USER root

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY ./leadquelle /mnt/extra-addons/leadquelle
COPY ./account_ext /mnt/extra-addons/account_ext
COPY ./modern_theme /mnt/extra-addons/modern_theme
COPY ./om_account/accounting_pdf_reports /mnt/extra-addons/accounting_pdf_reports
COPY ./om_account/om_account_accountant /mnt/extra-addons/om_account_accountant
COPY ./om_account/om_account_asset /mnt/extra-addons/om_account_asset
COPY ./om_account/om_account_bank_statement_import /mnt/extra-addons/om_account_bank_statement_import
COPY ./om_account/om_account_budget /mnt/extra-addons/om_account_budget
COPY ./om_account/om_account_daily_reports /mnt/extra-addons/om_account_daily_reports
COPY ./om_account/om_account_followup /mnt/extra-addons/om_account_followup
COPY ./om_account/om_fiscal_year /mnt/extra-addons/om_fiscal_year
COPY ./om_account/om_recurring_payments /mnt/extra-addons/om_recurring_payments
COPY ./base_accounting_kit/base_accounting_kit /mnt/extra-addons/base_accounting_kit
COPY ./base_accounting_kit/base_account_budget /mnt/extra-addons/base_account_budget

RUN apt-get install -y wkhtmltopdf

ENTRYPOINT ["/entrypoint.sh"]
CMD ["-d", "leadquelle-odoo", "-u", "leadquelle_user", "--workers", "8", "--no-database-list"]