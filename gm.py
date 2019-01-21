import argparse, configparser, os, sys, urllib.request


gmdir = '.gm'
gmini = gmdir + '\info.ini'
gmgma = gmdir + '\\tmp.gma'
files = {
'addon.json' : '''{
	"title"		:	"Example Addon",
	"type"		:	"ServerContent",
	"tags"		:	[ "roleplay", "realism" ],
	"ignore"	:
	[
		"*.psd",
		"*.jpg",
		"*.txt",
		"README.md",
		"*.vcproj",
		"*.svn*",
		".git*",
		".gm*",
		"*.gma"
	]
}''',
'README.md' : '''Example Addon

[h1]Features:[/h1]
[list]
[*][b]Feature 1[/b] - Lorem ipsum dolor sit amet...
[/list]

[h1]If you enjoyed this addon, leave a like and favorite![/h1]
[img]https://i.imgur.com/Gkw7mwm.gif[/img]'''
}
gmbin = os.path.dirname(os.path.realpath(__file__))

def exe(cmd, *args):
		return os.system(gmbin + '\\' + cmd + '.exe ' + ' '.join(args)) == 0


class GM(object):

	def __init__(self):
		self.cfg = configparser.ConfigParser()
		if os.path.isfile(gmini):
			self.cfg.read(gmini)
		self.parser = argparse.ArgumentParser(
			description='Garry\'s Mod addon utility.',
			usage='''gm <command> [<args>]

The most commonly used GM commands are:
   config  Set config variables
   deinit  Deinitialize GM workspace
   icon	   Update addon\'s icon on the workshop
   init	   Initialize GM workspace
   push	   Push your addon to the workshop
   reset   Set the local repository to an unpublished state
   update  Update this script to the latest version
''')
		self.parser.add_argument('command', help='Subcommand to run')
		args = self.parser.parse_args(sys.argv[1:2])
		if not hasattr(self, args.command):
			print('Unrecognized command')
			self.parser.print_help()
			exit(1)
		getattr(self, args.command)()
		if os.path.isdir(gmdir):
			with open(gmini, 'w') as configfile:
				self.cfg.write(configfile)
			
	def init(self):
		self.parser = argparse.ArgumentParser(
			description='Deinitialize GM workspace')
		if not os.path.isdir(gmdir):
			os.mkdir(gmdir)
			os.system('attrib +h ' + gmdir)
			for path, contents in files.items():
				if not os.path.isfile(path):
					with open(path, 'w') as f:
						f.write(contents)
			self.cfg['workshop'] = {}
			self.cfg['workshop']['id'] = ''
			self.cfg['workshop']['published'] = 'false'
			print('Initialized GM workspace')
		else:
			print('GM workspace already exists')
			
	def deinit(self):
		self.parser = argparse.ArgumentParser(
			description='Deinitialize GM workspace')
		if os.path.isdir(gmdir):
			shutil.rmtree(gmdir)
			print('Deinitialized GM workspace')
		else:
			print('GM workspace does not exist')
	
	def icon(self):
		self.parser = argparse.ArgumentParser(
			description='Update addon\'s icon on the workshop')
		if self.cfg['workshop']['published'] == 'false':
			id = self.cfg['workshop']['id']
			if id:
				print('Updating icon...')
				exe('gmpublish', 'update -icon', '"' + os.path.realpath('icon.jpg') + '"', '-id', id)
				print('Updated icon!')
			else:
				print('To update your addon\'s icon on the workshop you must set the addon id with the command \'gm config --id <id>\'. The number after the \'?id=\' of the workshop page url is the addon id.')
		else:
			print('You need to publish your addon before updating the icon.')
		
	def push(self):
		self.parser = argparse.ArgumentParser(
			description='Push your addon to the workshop')
		if self.cfg['workshop']['published'] == 'false':
			print('Packaging addon...')
			if exe('gmad', 'create -folder', '"' + os.path.realpath(os.getcwd()) + '"', '-out', '"' + os.path.realpath(gmgma) + '"'):
				print('Packaged addon!')
				print('Publishing addon...')
				if exe('gmpublish', 'create -addon', '"' + os.path.realpath(gmgma) + '"', '-icon', '"' + os.path.realpath('icon.jpg') + '"'):
					self.cfg['workshop']['published'] = 'true'
					print('Published addon!')
					print('If you want to update your addon on the workshop in the future, you must set the addon id with the command \'gm config --id <id>\'. The number after the \'?id=\' of the workshop page url is the addon id.')
				else:
					print('Failed to publish addon.')
			else:
				print('Failed to package addon.')
		else:
			id = self.cfg['workshop']['id']
			if id:
				self.parser.add_argument('-m')
				args = self.parser.parse_args(sys.argv[2:])
				print('Packaging addon...')
				if exe('gmad', 'create -folder', '"' + os.path.realpath(os.getcwd()) + '"', '-out', '"' + os.path.realpath(gmgma) + '"'):
					print('Packaged addon!')
					print('Updating addon...')
					if args.m:
						r = exe('gmpublish', 'update -addon', '"' + os.path.realpath(gmgma) + '"', '-id', id, '-changes', args.m)
					else:
						r = exe('gmpublish', 'update -addon', '"' + os.path.realpath(gmgma) + '"', '-id', id)
					if r:
						print('Updated addon!')
					else:
						print('Failed to update addon.')
				else:
					print('Failed to package addon.')
			else:
				print('To update your addon on the workshop you must set the addon id with the command \'gm config --id <id>\'. The number after the \'?id=\' of the workshop page url is the addon id.')
				
	def reset(self):
		if self.cfg['workshop']['published'] == 'true':
			self.cfg['workshop']['id'] = ''
			self.cfg['workshop']['published'] = 'false'
			print('Reset the local repository! You must manually remove the workshop page.')
		else:
			print('The addon has not been published.')
	
	def config(self):
		self.parser = argparse.ArgumentParser(
			description='Set config variables')
		self.parser.add_argument('--id')
		args = self.parser.parse_args(sys.argv[2:])
		if len(sys.argv) > 2:
			if args.id:
				if args.id.isdigit():
					self.cfg['workshop']['id'] = args.id
					self.cfg['workshop']['published'] = 'true'
					print('Set workshop id to ' + args.id)
				else:
					print('id must be a number')
		else:
			for arg in vars(args):
				print(arg + ' = ' + self.cfg['workshop'][arg])
	
	def update(self):
		self.parser = argparse.ArgumentParser(
			description='Update this script to the latest version')
		print('Updating script...')
		stream = urllib.request.urlopen("https://raw.githubusercontent.com/prowolf/gm/master/gm.py")
		raw = stream.read()
		stream.close()
		data = raw.decode("utf8")
		with open(__file__, 'w') as f:
			f.write(data)
		print('Updated script!')


if __name__ == '__main__':
	GM()
