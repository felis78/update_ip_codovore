# Update ip pour serveur autohebergé

## Utilité:

Sert à mettre à jour automatiquement l'ip de la zone dns pointant vers un serveur personnel, via l'api Infomaniak. En effet,
les fournisseurs d'acces changent l'ip externe des boxes. Ce programme permet de passer outre simplement cet inconvenient quand on
heberge un serveur chez sois

## Utilisation:

Pour l'utiliser il faut: 

- un nom de domaine enregistré chez infomaniak
- Une clé api Infomaniak
- l'id de l'enregistrement dns à modifier.

## Fonctionnement

Le programme va chercher l'ip locale via un site d'affichage d'ip, et l'ip enregistrée sur infomaniak. Si les ip sont 
différentes, il met à jour celle sur infomaniak