import logging
import werkzeug
from werkzeug.urls import url_encode

from odoo import http, tools, _
from odoo.addons.auth_signup.models.res_users import SignupError
from odoo.addons.web.controllers.home import ensure_db, Home, SIGN_UP_REQUEST_PARAMS, LOGIN_SUCCESSFUL_PARAMS
from odoo.addons.base_setup.controllers.main import BaseSetup
from odoo.exceptions import UserError
from odoo.http import request
import random
_logger = logging.getLogger(__name__)

class AuthSignupHome(Home):


	@http.route(['/web/uasg-signup'], type='http', auth="public",website=True,methods=['POST'])

	def send_otp(self,**post) : 


		otp = random.randint(1111,9999)
		sms_config = request.env['sms.configuration'].search([('active','=',True)],limit=1)
		
		message="OTP ="+str(otp)
		values = {
		'name' : post.get('name'),
		'login' : post.get('login'),
		'mobile' : post.get('mobile'),
		'otp' : otp,
		'token' : post.get('token')
		}

		sms_config.send_sms(message,post.get('mobile'))
		_logger.info(str('ssssssssssssssssssss'+str(otp)+'ddddddddddddddddddddd'+str(post.get('mobile'))))
		return request.render('uasg_customer_signup.otp_verifiy',values)



	@http.route(['/verify/otp'], type='http', auth="public",website=True,methods=['POST'])

	def verify_otp(self,**post) : 


		if post.get('otp') == post.get('otp2') :

			values = {'login' : post.get('login') , 'password' : 123 , 'name' : post.get('name')} 
			token = post.get('token')
			login, password = request.env['res.users'].sudo().signup(values, token)

			request.env.cr.commit()     # as authenticate will use its own cursor we need to commit the current transaction
			pre_uid = request.session.authenticate(request.db, login, password)
			return request.redirect('/web')
		else:
				raise SignupError(str('op1 = '+post.get('otp')+'opt 2 ='+post.get('otp2')))
