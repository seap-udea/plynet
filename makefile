
BRANCH=$(shell bash .getbranch)

clean:
	@echo "Cleaning directory..."
	@find . -name "*~" -exec rm -rf {} \;
	@find . -name "*#*" -exec rm -rf {} \;
	@find . -name "*.pyc" -exec rm -rf {} \;
	@find . -name "screenlog*" -exec rm -rf {} \;

commit:
	@echo "Committing changes to branch $(BRANCH)..."
	@git commit -am "Commit"
	@git push origin $(BRANCH)

pull:
	@echo "Getting the lattest changes from branch $(BRANCH)..."
	@git reset --hard HEAD	
	@git pull origin $(BRANCH)

edit:
	emacs -nw makefile plynet/*.py plynet/*.cfg

branch:
	@echo $(BRANCH)
