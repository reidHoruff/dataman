import os, sys, datetime
import MySQLdb

try:
	import socrates.settings as settings
except:
	print "Error: %s is not in the correct directory, cannot find settings.py" % __file__
	sys.exit(1)


if settings.DATABASES['default']['ENGINE'] != 'django.db.backends.mysql':
	print 'data base not mySQL'
	sys.exit(1)

db_name = settings.DATABASES['default']['NAME']
db_user = settings.DATABASES['default']['USER']
db_pass = settings.DATABASES['default']['PASSWORD']
now = datetime.datetime.now()

def make_query(queries=()):
	try:
		db = MySQLdb.connect("localhost", db_user, db_pass)
	except:
		print "unable to connect to database"
		sys.exit(1)

	cursor = db.cursor()

	for query in queries:
		print "query: %s" % (query)
		try:
			cursor.execute(query)
		except:
			print "invalid query"
			sys.exit(1)

	db.close()
	

def dump(dump_dir=None):

	if dump_dir is None:
		dump_dir = '%s_%s-%s-%s_%s:%s.sql' % (db_name, now.month, now.day, now.year, now.hour, now.minute)

	dump_cmd = "mysqldump --add-drop-table -u %s -p%s %s > %s" % (db_user, db_pass, db_name, dump_dir)

	print "dumping database '%s' through %s@%s to %s" % (db_name, db_user, db_pass, dump_dir)
	print "cmd: %s" % (dump_cmd)

	os.system(dump_cmd)

def restore(read_dir):

	queries = (
		"CREATE DATABASE IF NOT EXISTS %s" % db_name,
	)

	make_query(queries)

	build_cmd = "mysql -u %s -p%s %s < %s" % (db_user, db_pass, db_name, read_dir)

	print "building database '%s' through %s@%s from %s" % (db_name, db_user, db_pass, read_dir)
	print "cmd: %s" % (build_cmd)

	os.system(build_cmd)

def drop():
	queries = (
		"DROP DATABASE IF EXISTS %s" % db_name,
	)

	make_query(queries)

def create():
	queries = (
		"CREATE DATABASE %s" % db_name,
	)

	make_query(queries)


def clear():
	queries = (
		"DROP DATABASE IF EXISTS %s" % db_name,
		"CREATE DATABASE %s" % db_name,
	)

	make_query(queries)

def sync():	
	execfile("manage.py syncdb")

def help():
	print "help"
	print "--dump"
	print "--dump [filename.sql]"
	print "--restore [filename.sql]"
	print "--clear"
	print "--create"
	print "--drop"
	print "--syncdb"

if __name__ == '__main__':

	len = len(sys.argv)

	if len <= 1:
		help()

	elif sys.argv[1] == "--dump":
		if len >= 3:
			dump(sys.argv[2])

		else:
			dump()

	elif sys.argv[1] == "--restore" and len >= 3:
		restore(sys.argv[2])

	elif sys.argv[1] == "--clear":
		clear()

	elif sys.argv[1] == "--create":
		create()

	elif sys.argv[1] == "--drop":
		drop()

	elif sys.argv[1] == "--sync":
		print "still working on this"
		#sync()

	else:
		help()

