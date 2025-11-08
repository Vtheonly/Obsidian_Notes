### connect and configure a router a with  PC

1. console a cable the cyan blue cable
2. then in the PC the input port is  `RS232` 
3. then in the router in the console input 
4. then click the PC 
5. then terminal
6. then OK
7. then no
8. done

what is the interface mode in a router 
on  a router interface there is 

1. the  gigabytes Ethernet
2. the series
3. and fast Ethernet

the difference   is the speed / debit between the fast and the gigabyte the fast and gigabyte are to connect to anything with the route like a PC with a router and switch with a router and the the series is  to connect 2 routers



### then there is the terminal to configure a router
```
Router> //normal
Router# //previllaged
Router#(config) //configutrer gollable
Router(config-if)# //configuitre inteface 
Router(line)# //configre line
```

what to do from here on out



```

1 Université M’hamed Bougara de Boumerdes / Faculté des Sciences / Département d’Informatique Module : Réseaux Avancés Responsable: Dr. S.HAMADOUCHE Niveau : Master 1 Année Universitaire : 2025-2026 TP 02 : Configuration d’un routeur Objectif : le but de ce TP est :  Se familiariser avec le mode setup du routeur  S’initier à la configuration de base d’un routeur  Configuration des interfaces Ethernet d’un routeur Partie 01 : Prise en main d’un routeur Rappel : La configuration d’un équipement réseau se fait à travers une console (un PC) connectée à l’équipement soit par un câble console soit directement par une session telnet dans le cas où l’interface réseau est activée et possède une adresse IP. Généralement, la première fois ne peut se faire qu’à travers une console connectée directement sur l’équipement à configurer. Par défaut, on se connecte sur l’équipement réseau (switch ou routeur) en mode utilisateur qui permet uniquement la visualisation de la configuration courante. Pour avoir la possibilité de configuration, il faut passer en mode privilégié (super-utilisateur). Dans packet tracer, un routeur (ou un switch) peut être configuré de deux façons équivalentes: 1. Relier un PC au routeur à travers un câble console (interface : RS 232  console). Cliquer sur le PC  onglet ‘desktop’  terminal  cliquer sur ‘OK’  l’interface de configuration du routeur est affichée. 2. Directement à partir du routeur  cliquer dessus  onglet ‘CLI’  l’interface de configuration du routeur est affichée. Les différents modes d’utilisateurs • Mode Utilisateur: Permet de consulter toutes les informations liées au routeur sans pouvoir les modifier. Le shell est le suivant : Router > • Utilisateur privilégié : Permet de visualiser l'état du routeur et d'importer/exporter des images d'IOS. Le shell est le suivant : Router # • Mode de configuration globale : Permet d’utiliser les commandes de configuration générales du routeur. Le shell est le suivant : Router (config) # • Mode de configuration d’interfaces: Permet d’utiliser des commandes de configuration des interfaces (Adresses IP, masque, etc.). Le shell est le suivant : Router (config-if) # • Mode de configuration de ligne : Permet de configurer une ligne (exemple: accès au routeur par Telnet). Le shell est le suivant : Router (config-line) # Les principales commandes de configuration sont résumées ci-dessous : 1. Changer le nom du routeur (à partir du mode de configuration globale) Router > enable Router # configure terminal Router (config) # Router (config) #hostname NouveauNom 2. Application d’un mot de passe à l’accès Privilégié Router (config) # enable password mot_de_passe 3. Configuration de l'accès Telnet au routeur La configuration avec le câble console et HyperTerminal n’étant pas très pratique, il est possible d'autoriser les administrateurs à se connecter au routeur via une session Telnet à partir de n'importe quel poste des réseaux connectés au routeur. 2 Passez d'abord en mode de configuration globale, puis en mode de configuration de ligne VTY: Router > enable Password?: Router # configure terminal Router (config) # line vty 0 4 (pour configurer la possibilité de 5 sessions telnet simultanées sur ce routeur.) Pour activer le Telnet, il suffit d'appliquer un mot de passe à la ligne: Router (config-line) # password mot_de_passe Router (config-line) # login Router (config-line) # exit 4. Commandes d'information (à partir du mode privilégié)  Afficher le fichier de configuration courante du routeur: show running-config  Afficher les informations sur la configuration matérielle du système et sur l'IOS: show version  Afficher les protocoles configurés de couche 3 du modèle OSI : show protocols  Afficher la table de routage IP : show ip route  Afficher des informations sur une interface : show interface nom_interface  Afficher des informations sur toutes les interfaces : show interfaces 5. Commandes d'enregistrement de la configuration courante Ces commandes permettent de sauvegarder la configuration actuelle pour l’appliquer automatiquement en cas de redémarrage du routeur. Elles s’exécutent en mode Privilégié  Sauvegarde avec demande de confirmation: copy running-config startup-config  Sauvegarde sans demande de confirmation: write 6. Commande d'annulation Cette commande permet de revenir à la dernière configuration enregistrée, annulant toutes les modifications ayant été faites à la configuration depuis. Elle s'exécute en mode Privilégié. copy startup-config running-config 7. Annulation d'une commande particulière Pour annuler une commande particulière, on utilisera le préfixe no devant la commande précédemment exécutée. 8. Commandes d’interfaces Ces commandes sont liées à la configuration des interfaces du routeur (à partir du mode de configuration d’interface) • Attribution d’une adresse IP à une interface Ethetnet: Router > enable Router # configure terminal Router (config) # interface nom_interface Router (config-if) # ip address @IP masque • Activation de l'interface (obligatoire après l’étape précédente): no shutdown 3  Attribution d’une adresse IP à une interface Série: Router (config) # interface interface_name (for example: Serial 0/0/0) Router (config-if) # ip address IP@ mask Router (config-if) #clock rate …… (for example: 56000) Router (config-if) # no shutdown Partie 02 : Configuration des interfaces Ethernet d’un routeur (Exercice) Soit la topologie de base suivante : Supposons que PC1 soit connecté au routeur via l'interface fa 0/0 et PC2 via l'interface fa0/1. Configuration IP des PC PC 1: • Adresse IP/Masque: 192.168.1.1/24 • Passerelle: Ce sera l’adresse IP de l'interface du routeur à laquelle est connectée le PC (prendre la dernière adresse utilisable) PC 2: • Adresse IP/Masque: 10.0.0.1/8 • Passerelle: Ce sera l’adresse IP de l'interface du routeur à laquelle est connectée le PC (prendre la dernière adresse utilisable) Questions : 1. Vérifiez la connectivité entre PC1 et PC2. Expliquez les résultats. 2. Connectez le câble de la console entre le routeur et l'ordinateur à utiliser pour la configuration, puis répétez les instructions de base précédentes (partie1). 3. Ensuite, nous devons faire communiquer les deux réseaux connectés au routeur. Pour cela, configurez les interfaces Ethernet du routeur à l'aide des commandes adéquates. 4. Vérifier la connectivité entre PC1 et PC2. Remarque : Pensez toujours à enregistrer la configuration courante à l’aide de la commande prévue à cet effet.
```