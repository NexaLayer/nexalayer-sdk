.PHONY: install-py install-node test-py test-node lint clean

install-py:
	cd python && pip install -e ".[dev]"

install-node:
	cd node && npm install

test-py:
	cd python && pytest -v

test-node:
	cd node && npm test

lint:
	cd python && black python/nexalayer python/tests
	cd node && npm run lint 2>/dev/null || true

clean:
	rm -rf python/build python/dist python/*.egg-info
	rm -rf node/dist node/node_modules
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
