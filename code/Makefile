all: build

install:
	pipenv install

install-dev:
	pipenv install --dev

executable:
	pyinstaller stego_lsb.py --onefile

clean:
	rm -rf dist build
