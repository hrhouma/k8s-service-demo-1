# Tutoriel pour Déployer une Application sur Minikube avec un Seul Nœud

Ce tutoriel vous guidera à travers les étapes pour déployer une application Flask avec une base de données MySQL et Redis sur un cluster Kubernetes utilisant Minikube.

## Prérequis
- Docker installé
- Minikube installé
- `kubectl` installé

![Architecture](https://github.com/janakiramm/Kubernetes-multi-container-pod/blob/master/multi-container-pod.png?raw=true)

## Étapes

### 1. Installer Minikube et Configurer le Cluster

Ouvrez un terminal et exécutez les commandes suivantes pour configurer Minikube et démarrer un cluster avec un seul nœud :

```sh
sudo -s
minikube delete
minikube start --driver=docker
kubectl cluster-info
```



### 2. Cloner le Projet

Clonez le dépôt Git contenant le projet :

```sh
git clone https://github.com/hrhouma/k8s-service-demo-1.git
cd k8s-service-demo-1/
```

```sh
sudo apt update
sudo apt install python3.10
python3.10 --version
sudo apt install python3-pip
pip3 --version
pip3 install flask redis mysql-python
```
### 3. Construire et Taguer les Images Docker

Construisez les images Docker nécessaires et taguez-les :

```sh
cd build
docker-compose up -d # Optionnel
# OU
docker build . -t hrehouma1/flaskapp:1.2

docker images

docker tag redis:latest hrehouma1/redis:1.2
docker tag mysql:latest hrehouma1/mysql:1.2
docker tag build_web hrehouma1/flaskapp:1.2 # Exemples
```

### 4. Pousser les Images vers Docker Hub

Poussez les images Docker vers votre registre Docker Hub :

```sh
docker push hrehouma1/redis:1.2
docker push hrehouma1/mysql:1.2
docker push hrehouma1/flaskapp:1.2

docker ps
docker images
```

### 5. Déployer les Services sur Kubernetes

Appliquez les fichiers de déploiement et de service Kubernetes :

```sh
cd ../deploy
kubectl apply -f db-deployment.yaml
kubectl apply -f db-svc.yml
kubectl apply -f web-deployment.yaml
kubectl apply -f web-svc.yml
```

### 6. Vérifier les Déploiements et Services

Vérifiez que vos pods, services et déploiements sont actifs :

```sh
kubectl get pods
kubectl get svc
kubectl get deployments

# Remplacer 'web-58d5b669c5-nkgrj' et 'mysql' par les noms de vos pods
kubectl logs web-58d5b669c5-nkgrj
kubectl logs mysql
```

### 7. Tester l'Application

Déterminez l'adresse IP du nœud et le port du service pour accéder à votre application :

```sh
minikube ip
export NODE_IP=$(minikube ip)
export NODE_PORT=$(kubectl get svc web -o jsonpath='{.spec.ports[0].nodePort}')
```

Testez les endpoints de votre application Flask :

```sh
curl http://$NODE_IP:$NODE_PORT/init
curl -i -H "Content-Type: application/json" -X POST -d '{"uid": "1", "user":"Haythem Rehouma"}' http://$NODE_IP:$NODE_PORT/users/add
curl http://$NODE_IP:$NODE_PORT/users/1
```

### 8. Supprimer les Déploiements et Services

Nettoyez vos déploiements Kubernetes en supprimant les services et déploiements :

```sh
kubectl delete -f db-deployment.yaml
kubectl delete -f db-svc.yml
kubectl delete -f web-deployment.yaml
kubectl delete -f web-svc.yml

minikube delete

exit
exit
```

### 9. Ajouter d'autres Utilisateurs (Exemples)

Vous pouvez également ajouter d'autres utilisateurs avec des commandes `curl` :

```sh
curl -i -H "Content-Type: application/json" -X POST -d '{"uid": "1", "user":"Haythem Rehouma"}' http://$NODE_IP:$NODE_PORT/users/add
curl -i -H "Content-Type: application/json" -X POST -d '{"uid": "2", "user":"John Doe"}' http://$NODE_IP:$NODE_PORT/users/add
curl -i -H "Content-Type: application/json" -X POST -d '{"uid": "3", "user":"Jane Smith"}' http://$NODE_IP:$NODE_PORT/users/add
curl -i -H "Content-Type: application/json" -X POST -d '{"uid": "4", "user":"Mike Taylor"}' http://$NODE_IP:$NODE_PORT/users/add
curl http://$NODE_IP:$NODE_PORT/users/1
```

### 10. Ajouter des Utilisateurs avec Emojis

Ajoutez des utilisateurs avec des emojis pour rendre les données plus amusantes et visuelles :

```sh
curl -i -H "Content-Type: application/json" -X POST -d '{"uid": "1", "user":"Haythem Rehouma 😊"}' http://$NODE_IP:$NODE_PORT/users/add
curl -i -H "Content-Type: application/json" -X POST -d '{"uid": "2", "user":"John Doe 🚀"}' http://$NODE_IP:$NODE_PORT/users/add
curl -i -H "Content-Type: application/json" -X POST -d '{"uid": "3", "user":"Jane Smith 🌟"}' http://$NODE_IP:$NODE_PORT/users/add
curl -i -H "Content-Type: application/json" -X POST -d '{"uid": "4", "user":"Mike Taylor 🎉"}' http://$NODE_IP:$NODE_PORT/users/add
curl http://$NODE_IP:$NODE_PORT/users/1
```

En suivant ces étapes, vous aurez déployé avec succès une application Flask sur un cluster Minikube avec un seul nœud, utilisant MySQL et Redis comme services de base de données et de cache.
