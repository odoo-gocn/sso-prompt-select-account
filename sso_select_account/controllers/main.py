from odoo.addons.auth_oauth.controllers.main import OAuthLogin
from odoo.http import request
import json
import werkzeug.urls

class CustomOAuthLogin(OAuthLogin):

    def list_providers(self):
        try:
            providers = request.env['auth.oauth.provider'].sudo().search_read([('enabled', '=', True)])
        except Exception:
            providers = []

        for provider in providers:
            return_url = request.httprequest.url_root + 'auth_oauth/signin'
            state = self.get_state(provider)

            params = dict(
                response_type='token',
                client_id=provider['client_id'],
                redirect_uri=return_url,
                scope=provider['scope'],
                state=json.dumps(state),
                prompt='select_account',
            )

            auth_endpoint = provider['auth_endpoint'].rstrip('?')
            sep = '&' if '?' in auth_endpoint else '?'
            provider['auth_link'] = "%s%s%s" % (
                auth_endpoint,
                sep,
                werkzeug.urls.url_encode(params)
            )

        return providers
