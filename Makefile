.PHONY: release

release:
ifndef version
	$(error ❌ Missing version. Usage: make release version=0.2.0)
endif

	@echo "🔧 Updating version to $(version) in pyproject.toml..."
	sed -i.bak "s/^version = \".*\"/version = \"$(version)\"/" pyproject.toml
	rm -f pyproject.toml.bak

	@echo "📦 Committing version bump..."
	git add pyproject.toml
	git commit -m "Bump version to $(version)"

	@echo "🏷️ Creating tag v$(version)..."
	git tag v$(version)

	@echo "🚀 Pushing tag (will trigger PyPI publish)..."
	git push origin v$(version)

	@echo "🎉 Done! GitHub Actions will now publish v$(version)."
