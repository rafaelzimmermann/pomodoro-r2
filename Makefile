

clean:
	./scripts/clean.sh


deploy: clean
	./scripts/deploy-dir.sh .
