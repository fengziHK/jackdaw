
from jackdaw.dbmodel.adinfo import JackDawADInfo
from jackdaw.dbmodel.tokengroup import JackDawTokenGroup
from jackdaw.dbmodel import *

from pyvis.network import Network


class MembershipPlotter:
	def __init__(self, db_conn):
		self.db_conn = db_conn
		self.graph = Network()
		self.show_group_memberships = True
		self.show_user_memberships = True
		self.show_machine_memberships = True
		self.show_session_memberships = True
		
	def run(self, ad_id):
		session = get_session(self.db_conn)
		adinfo = session.query(JackDawADInfo).get(ad_id)
		
		node_lables = {}
		node_color_map = []
		
		distinct_filter = {}
		if self.show_user_memberships == True:
			#adding group nodes
			for group in adinfo.groups:
				if group.sid in distinct_filter:
					continue
				distinct_filter[group.sid] = 1
				self.graph.add_node(group.sid, label=group.name, color="#00ff1e")
		
		distinct_filter = {}
		if self.show_user_memberships == True:
			#adding user nodes
			for user in adinfo.users:
				if user.objectSid in distinct_filter:
					continue
				distinct_filter[user.objectSid] = 1
				
				self.graph.add_node(user.objectSid, label=user.sAMAccountName, color="#162347")
				
		distinct_filter = {}
		if self.show_machine_memberships == True:
			#adding user nodes
			for user in adinfo.computers:
				if user.objectSid in distinct_filter:
					continue
				distinct_filter[user.objectSid] = 1
				self.graph.add_node(user.objectSid, label= user.sAMAccountName, color="#dd4b39")
		
		"""
		if self.show_session_memberships == True:
			session.query(
			
			
			
			source = Column(String, index=True)
			ip = Column(String, index=True)
			rdns = Column(String, index=True)
			username = Column(String, index=True)
		"""
		#adding membership edges
		distinct_filter = {}
		for tokengroup in adinfo.group_lookups:
			if tokengroup.sid in distinct_filter:
				continue
			distinct_filter[tokengroup.sid] = 1
			if tokengroup.is_user == True and self.show_user_memberships == True:
				try:
					self.graph.add_edge(tokengroup.sid, tokengroup.member_sid)
				except AssertionError as e:
					print(e)
			elif tokengroup.is_machine == True and self.show_machine_memberships == True:
				try:
					self.graph.add_edge(tokengroup.sid, tokengroup.member_sid)
				except AssertionError as e:
					print(e)
			elif tokengroup.is_group == True and self.show_group_memberships == True:
				try:
					self.graph.add_edge(tokengroup.sid, tokengroup.member_sid)
				except AssertionError as e:
					print(e)
		self.graph.show("gameofthrones.html")