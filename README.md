Ceci est un fichier qui a pour but d'informer les participants au projet.

Concernant git:
	-Si vous souhaitez ajouter une fonctionnalité, il est important de créer un branche git dédiée (git branch <name>).
	Ensuite vous pouvez vous déplacer sur une branche et commencer à y travailler. Cependant il est important de ne pas modifier le contenu de la branche mère.
	-Quand vous désirez enregistrer un ajout sur un branche (ex: a la fin d'une séance) vous pouvez créer un nouveau point sur la branche sur laquelle vous travaillez en enregistrant un "commit".
	Pour se faire, utilisez la commande "git add -A", qui ajoutera tous les fichiers à votre commit. Si vous ne souhaitez ajouter que certains fichiers au commit que vous préparez, préferez la commande "git add <files>", où vous ne spécifiez que les fichiers que vous avez modifié.
	Après avoir préparer le commit enregistrez le en utilisant "git commit -m "<msg>"", ou vous remplacez <msg> par un brève description du commit.
	-Une fois le but d'une branche atteint vous pouvez retourner sur la branche mère et "merge" la branche fille sur la branche mère. Avant de se faire soyez sur qu'il n'y aura pas de conflits.
	Une fois sur la branche mère utlisez la commande "git merge <branch_name>" en remplacant <branch_name> par le nom de la branche fille.

PARTI DEDIÉE AUX UTILISATEURS DU PROJET (Professeurs) :
	! -> Avant de pouvoir utiliser ce projet ayez télécharger sur votre ordinateur une version de python ainsi que le module <pgzero>
	Ce projet comporte un script menu qu'il est necessaire de lancer pour jouer au projet. Cliquez simplement sur le bouton jouer pour dirigez Pac Man à l'aide des flèches directionnelles.
	Les points vous donnent des des points, et les gros points 5 points d'un coup. On ne peut pas gagner réellement, le but est de ramasser un maximum de points.
	Le fantome rouge, Blinky, vous traquera à l'aide de l'aglorithme A*, le fantome orange, Clyde, se déplace de facon aléatoire mais fuit en haut à gauche quand vous êtes trop près de lui.
	Le projet comporte également un script LevelEditor.py dans le dossier map qui permet d'editer la map. Clique gauche pour rajouter/enlever des murs et le clique droit pour ajouter/supprimer des gros points. Puis entrez <ENTRER> pour enregister les modifications.
	CEPENDANT le système ne tolère que certains patternes pour les murs, faites des formes simples au possible.