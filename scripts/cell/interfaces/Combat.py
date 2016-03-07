# -*- coding: utf-8 -*-
import KBEngine
import GlobalDefine
import random
from KBEDebug import * 
from interfaces.CombatPropertys import CombatPropertys

class Combat(CombatPropertys):
	"""
	关于战斗的一些功能
	"""
	def __init__(self):
		CombatPropertys.__init__(self)
		
	def canUpgrade(self):
		"""
		virtual method.
		"""
		return True
		
	def upgrade(self):
		"""
		for real
		"""
		if self.canUpgrade():
			self.addLevel(1)
			
	def addLevel(self, lv):
		"""
		for real
		"""
		self.level += lv
		self.onLevelChanged(lv)
		
	def isDead(self):
		"""
		"""
		return self.state == GlobalDefine.ENTITY_STATE_DEAD
		
	def die(self, killerID):
		"""
		"""
		if self.isDestroyed or self.isDead():
			return
		
		if killerID == self.id:
			killerID = 0
			
		INFO_MSG("%s::die: %i i die. killerID:%i." % (self.getScriptName(), self.id, killerID))
		killer = KBEngine.entities.get(killerID)
		if killer:
			killer.onKiller(self.id)
			
		self.onBeforeDie(killerID)
		self.onDie(killerID)
		self.changeState(GlobalDefine.ENTITY_STATE_DEAD)
		self.onAfterDie(killerID)
		if self.isMonster():
			if random.randint(0, 1) == 1:#掉落概率是10
<<<<<<< HEAD
				self.dropNotify(11,1)#(random.randint(1, 11),1)
=======
				self.dropNotify(11,3)#(random.randint(1, 11),1)
>>>>>>> d8f93ec982c0abf37db214a8f49061c6ecd95445
			killer.exp += random.randint(1, 10)
			if killer.exp > killer.level*5+20:
				killer.upgrade()
	
	def canDie(self, attackerID, skillID, damageType, damage):
		"""
		virtual method.
		是否可死亡
		"""
		return True
		
	def recvDamage(self, attackerID, skillID, damageType, damage):
		"""
		defined.
		"""
		if self.isDestroyed or self.isDead():
			return
		
		DEBUG_MSG("%s::recvDamage: %i attackerID=%i, skillID=%i, damageType=%i, damage=%i" % \
			(self.getScriptName(), self.id, attackerID, skillID, damageType, damage))
			
		if self.HP <= damage:
			if self.canDie(attackerID, skillID, damageType, damage):
				self.die(attackerID)
		else:
			self.setHP(self.HP - damage)
		
		self.allClients.recvDamage(attackerID, skillID, damageType, damage)
		
	def addEnemy(self, entityID, enmity):
		"""
		defined.
		添加敌人
		"""
		DEBUG_MSG("%s::addEnemy: %i entity=%i, enmity=%i" % \
						(self.getScriptName(), self.id, entityID, enmity))
		
		self.enemyLog.append(entityID)
		self.onAddEnemy(entityID)
		
	def removeEnemy(self, entityID):
		"""
		defined.
		删除敌人
		"""
		DEBUG_MSG("%s::removeEnemy: %i entity=%i" % \
						(self.getScriptName(), self.id, entityID))
		
		self.enemyLog.remove(entityID)
		self.onRemoveEnemy(entityID)
	
	def checkInTerritory(self):
		"""
		virtual method.
		检查自己是否在可活动领地中
		"""
		return True

	def checkEnemyDist(self, entity):
		"""
		virtual method.
		检查敌人距离
		"""
		dist = entity.position.distTo(self.position) <= 30.0
		if dist > 30.0:
			INFO_MSG("%s::checkEnemyDist: %i id=%i, dist=%f." % (self.getScriptName(), self.id, entity.id, dist))
			return False
		
		return True
		
	def checkEnemys(self):
		"""
		检查敌人列表
		"""
		for idx in range(len(self.enemyLog) - 1, -1, -1):
			entity = KBEngine.entities.get(self.enemyLog[idx])
			if entity is None or entity.isDestroyed or entity.isDead() or \
				not self.checkInTerritory() or not self.checkEnemyDist(entity):
				self.removeEnemy(self.enemyLog[idx])

	#--------------------------------------------------------------------------------------------
	#                              Callbacks
	#--------------------------------------------------------------------------------------------
	def onLevelChanged(self, addlv):
		"""
		virtual method.
		"""
		self.exp = 0
		self.strength = 15 + 1*self.level
		self.dexterity = 10 + 1*self.level
		self.base.updatePropertys()
		pass
		
	def onDie(self, killerID):
		"""
		virtual method.
		"""
		self.setHP(0)
		self.setMP(0)

	def onBeforeDie(self, killerID):
		"""
		virtual method.
		"""
		pass

	def onAfterDie(self, killerID):
		"""
		virtual method.
		"""
		pass
	
	def onKiller(self, entityID):
		"""
		defined.
		我击杀了entity
		"""
		pass
		
	def onDestroy(self):
		"""
		entity销毁
		"""
		pass
		
	def onAddEnemy(self, entityID):
		"""
		virtual method.
		有敌人进入列表
		"""
		pass

	def onRemoveEnemy(self, entityID):
		"""
		virtual method.
		删除敌人
		"""
		pass
