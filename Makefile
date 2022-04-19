

clean:
	./scripts/clean.sh


deploy: clean
	./scripts/deploy-dir.sh .


quick-deploy:
	./scripts/deploy-py.sh .
