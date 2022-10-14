Ceci est un fichier qui a pour but d'informer les participants au projet.

Concernant git:
	-Si vous souhaitez ajouter une fonctionnalité, il est important de créer un branche git dédiée (git branch <name>).
	Ensuite vous pouvez vous déplacer sur une branche et commencer à y travailler. Cependant il est important de ne pas modifier le contenu de la branche mère.
	-Quand vous désirez enregistrer un ajout sur un branche (ex: a la fin d'une séance) vous pouvez créer un nouveau point sur la branche sur laquelle vous travaillez en enregistrant un "commit".
	Pour se faire, utilisez la commande "git add -A", qui ajoutera tous les fichiers à votre commit. Si vous ne souhaitez ajouter que certains fichiers au commit que vous préparez, préferez la commande "git add <files>", où vous ne spécifiez que les fichiers que vous avez modifié.
	Après avoir préparer le commit enregistrez le en utilisant "git commit -m "<msg>"", ou vous remplacez <msg> par un brève description du commit.
	-Une fois le but d'une branche atteint vous pouvez retourner sur la branche mère et "merge" la branche fille sur la branche mère. Avant de se faire soyez sur qu'il n'y aura pas de conflits.
	Une fois sur la branche mère utlisez la commande "git merge <branch_name>" en remplacant <branch_name> par le nom de la branche fille.