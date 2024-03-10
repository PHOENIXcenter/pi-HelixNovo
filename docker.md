# Run pi-HelixNovo in Docker

- Setup the Docker Desktop
- Open Docker Desktop
- Sign in Docker Desktop (Sign up first if you don’t have an account)
- Open the CMD and running the following commands:

```jsx
docker pull ytp22/pi-helixnovo-env:v1
```

![Untitled](Run%20pi-HelixNovo%20in%20Docker%205593397d0c914f48b00fe13cfcc4a570/Untitled.png)

- Make a dir (c:/docker-share-dir) and put the pretrained model weights in it.

![Untitled](Run%20pi-HelixNovo%20in%20Docker%205593397d0c914f48b00fe13cfcc4a570/Untitled%201.png)

```jsx
docker run -it -v c:/docker-share-dir/:/data:rw --gpus all --shm-size 15G --name pi-HelixNovo ytp22/pi-helixnovo-env:v1 bash
```

![Untitled](Run%20pi-HelixNovo%20in%20Docker%205593397d0c914f48b00fe13cfcc4a570/Untitled%202.png)

```jsx
 cd /home/pi-HelixNovo/; conda activate main_env;
```

![Untitled](Run%20pi-HelixNovo%20in%20Docker%205593397d0c914f48b00fe13cfcc4a570/Untitled%203.png)

Note: /data dir corresponds to the c:/docker-share-dir dir

![Untitled](Run%20pi-HelixNovo%20in%20Docker%205593397d0c914f48b00fe13cfcc4a570/Untitled%204.png)

```jsx
python [main.py](http://main.py/) --mode=denovo --config=./config.yaml --gpu=0 --output=denovo.log --peak_path=./sample_data/denovo_sample/*.mgf --model=/data/MSV000081142-epoch-5-step-800000.ckpt
```

![Untitled](Run%20pi-HelixNovo%20in%20Docker%205593397d0c914f48b00fe13cfcc4a570/Untitled%205.png)

If the error “CUDA OUT OF MEMORY” occurs, please decrease the “predict_batch_size” in the config.yaml.

- Move the results to /data

```jsx
mv denovo_denovo.txt /data/
```

You will see the results in c:/docker-share-dir

![Untitled](Run%20pi-HelixNovo%20in%20Docker%205593397d0c914f48b00fe13cfcc4a570/Untitled%206.png)