from app import db

class Analysis(db.Model):
	__tablename__ = "analysis" # required

	analysis_ID = db.Column(db.Integer,primary_key=True) # required
	playerid = db.Column(db.String(9))
	playerName = db.Column(db.String(50))
	yearID = db.Column(db.Integer)
	birthYear = db.Column(db.Integer)
	birthMonth = db.Column(db.Integer)
	birthDay = db.Column(db.Integer)
	ageForYear = db.Column(db.Integer) #Age should be updated on every search
	stint = db.Column(db.Integer)
	team = db.Column(db.String(3))
	lgid = db.Column(db.String(2))
	G = db.Column(db.Integer)
	AB = db.Column(db.Integer)
	R = db.Column(db.Integer)
	H = db.Column(db.Integer)
	B2 = db.Column(db.Integer) # Make sure analysis has variable set this way
	B3 = db.Column(db.Integer) # Make sure analysis has variable set this way
	HR = db.Column(db.Integer)
	RBI = db.Column(db.Integer)
	SB = db.Column(db.Integer)
	CS = db.Column(db.Integer)
	BB = db.Column(db.Integer)
	SO = db.Column(db.Integer)
	IBB = db.Column(db.Integer)
	HBP = db.Column(db.Integer)
	SH = db.Column(db.Integer)
	SF = db.Column(db.Integer)
	GIDP = db.Column(db.Integer)
	OBP = db.Column(db.Numeric)
	SLG = db.Column(db.Numeric)
	TB = db.Column(db.Integer)
	RC = db.Column(db.Numeric)
	RC27 = db.Column(db.Numeric)
	PARC = db.Column(db.Numeric)
	PARC27 = db.Column(db.Numeric)
	W = db.Column(db.Numeric)
	SSB = db.Column(db.Numeric)
	TOB = db.Column(db.Numeric)
	OUTS = db.Column(db.Integer)
	PA = db.Column(db.Numeric)
	BA = db.Column(db.Numeric)

	def __repr__(self):
		return "<analysis(player='%s',yearid=%s, games=%s, RC27='%s')>" % (self.playerid, self.yearID, self.G, self.RC27)

	def setRC27(self):
		if self.RC is None:
			self.setRC()	
		outs=self.AB-self.H+self.coalesce(self.CS)+self.coalesce(self.SH)+self.coalesce(self.SF)+self.coalesce(self.GIDP)
		self.RC27 = 27 * self.RC/outs
		db.session.commit()

	def setRC(self):
		if self.OBP is None:
			self.setOBP()
		if self.TB is None:
			self.setTB()
		self.RC = self.OBP * self.TB

	def setOBP(self):
		onbase = self.H+self.BB+self.coalesce(self.HBP)
		pa = self.AB+self.BB+self.coalesce(self.HBP)+self.coalesce(self.SF)
		if pa == 0:
			self.OBP = 0
		else:
			self.OBP = onbase/pa

	def setTB(self):
		self.TB = self.H+self.B2+2*self.B3+3*self.HR

	def coalesce(self,x):
		if x is None:
			return 0
		else:
			return x

	def updateAge(self):
		#from june 30th of the year being pulled up
		if(self.birthMonth < 7):
			self.ageForYear = self.yearID - self.birthYear
		else:
			self.ageForYear = self.yearID - self.birthYear - 1
		db.session.commit()

class Web_Users(db.Model):
	__tablename__ = "webUsers" #Required

	webuser_ID = db.Column(db.Integer, primary_key=True) #Required
	username = db.Column(db.String(255))
	email = db.Column(db.String(255))
	# password_pt = db.Column(db.String(255))
	salt = db.Column(db.String(4))
	pw_hash = db.Column(db.String(255))

	def __repr__(self):
		return "<webUsers(uid='%s', username='%s', email='%s')>" % (self.webuser_ID, self.username, self.email)

	def checkInput(self):
   #TODO: need to build this for injection protection
		pass

class Saved_Searches(db.Model):
	__tablename__ = "savedSearches" #Required

	search_ID = db.Column(db.Integer, primary_key=True) #Required
	webuserID = db.Column(db.String(255))
	playerName = db.Column(db.String(255))
	playerID = db.Column(db.String(9))

	def __repr__(self):
		return "<savedSearches(searchID='%s', webuserID='%s', playerName='%s', playerID='%s')>" % (self.search_ID, self.webuserID, self.playerName, self.playerID)

class People(db.Model):
  __tablename__ = "people"
  
  playerID = db.Column(db.String(9), primary_key=True) #required
  nameFirst = db.Column(db.String(255))
  nameLast = db.Column(db.String(255))
  
  def __repr__(self):
    return "<people(playerID='%s', nameFirst='%s', nameLast='%s')>" % (self.playerID, self.nameFirst, self.nameLast)
  