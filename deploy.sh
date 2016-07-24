sudo docker build -t mypokemon .
sudo docker tag mypokemon:latest 816270155462.dkr.ecr.us-west-2.amazonaws.com/mypokemon:latest
sudo docker push 816270155462.dkr.ecr.us-west-2.amazonaws.com/mypokemon:latest
eb deploy
