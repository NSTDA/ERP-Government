ARG ODOO_VERSION
FROM ghcr.io/tecnativa/doodba:${ODOO_VERSION}-onbuild

# Change Directory Owner
USER root
RUN chown -R odoo:odoo /opt/odoo
USER odoo
