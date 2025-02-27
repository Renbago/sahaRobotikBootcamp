### 1. Build Docker Images

Bu komutu, önbelleğe alınmış bir katmanın sorunlara neden olduğunu düşünüyorsanız kullanabilirsiniz (örneğin, bağımlılıkların düzgün güncellenmemesi).
Ya da Dockerfile içinde yaptığınız değişikliklerin (apt-get veya benzer komutlar gibi) Docker’ın katman önbelleği tarafından tanınamayabileceğini düşünüyorsanız kullanabilirsiniz:

```docker-compose build --no-cache```

Uygulamanızda veya Dockerfile’da değişiklik yaptıysanız ve görüntüyü yeniden oluşturup konteynerları başlatmak istiyorsanız, bu komutu çalıştırmanız yeterlidir.

```docker-compose up -d --build``` 

### 2. Start Docker Containers:
```docker-compose up```, or ```docker-compose up -d``` 

### 3. Attach Visual Studio Code to Docker Container

1.Wsl de VSCode u aç.

2.Docker extension panel'e gel.

3.Çalışan container'ı bul

4.container a sağ tıkla ve **Attach Visual Studio Code**.

Bu adımlar Docker container'ı içindeki dosya sistemine bağlı bir Vsiual Studio Code açar. Yaptığınız uygulamaları doğrudan container içerisinde geliştirebilirsiniz.

### 4. SH

Terminal'e bağlanmak için: ``` docker exec -it ros_egitim_ws /bin/bash ```
