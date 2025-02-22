# Explanation

Merhabalar herkese, bu eğitimde kullanılan kaynakları burada yayınlayacağım. 
Eğitimin hedefi, github-wsl-docker gibi temel araçlarla başlayarak. Devamında takıldıgımız problemleri nasıl araştıracağımıza
ineceğim. Çünkü camia da aslında incelendiği zaman bir sürü ROS eğitimi bulunmakta fakat kimse bir proje yönetilmesi hususunda içerik üretmediği için Saha Robotik olarak eğitimde bu amacı gütmekteyiz.  

# Windows Users

Windows üzerinden ubuntu kullanmak için, Windows Subsytem Linux(wsl) 'in kurulum aşamalarını anlatacağım. Şu anda Ben de wsl + docker üzerinden ilerliyorum. 
Fakat bilgisayarınızı daha optimize kullanabilmek adına OS olarak ubuntu'yu tavsiye ederim. Eğer Kamera ile işlenecek projeler için wsl'i kullanacaksanız 
windows wsl'e porttan gelen datalar için erişim sağlattırmıyor. Bu hususta içinde OS olarak ubuntuya geçmeniz gerekir.  

# INSTALLATION STEPS

Wsl kurulumu için [text](https://learn.microsoft.com/en-us/windows/wsl/install), [video](https://www.youtube.com/watch?v=VUW2pIjDpEk)
version olarak ``` Ubuntu-22.04``` kullanıyoruz. Referans komut: ``` wsl.exe --install Ubuntu-22.04 ```

IDE olarak VSCode [installation](https://code.visualstudio.com/download) kullanıyorum. 

Docker [installation](https://docs.docker.com/engine/install/ubuntu/), docker kullanımını da windows docker yerine wsl de yapıyorum Tüm sistemim windowstan bağımsız olmuş oluyor.
Bunu linux sistemine bağlanmış olduğunuz terminalden çalıştırmanız gerekiyor.

extensions'lara iletmiş oldugum txt den teker teker indirebilirsiniz. 
Ya da extensions.txt nin bulunduğu dizine gidip ```cat extensions.txt | xargs -L 1 code --install-extension``` ile indirebilirsiniz.

# Windows shortcuts
Bir kaç tane kısayol ataması yaptım kullanımı iyileştirmesi adına, Kullandıgım [uygulama](https://www.autohotkey.com/) 
ubuntuda ki gibi direkt kısayolu olan ctrl+alt+t işlemini simüle etmek için atmış olduğum .ahk yı çalıştırabilirsiniz Ek olarak ctrl+c kodu durdurmayı
sağladığı için terminalde kullanımı çok uygun olmuyor bunu ctrl + shift + c 'ye atayabilirsiniz. bu atmış olduğum wsl_auto.ahk yı eğer 
Win + R kısmına, shell:startup yazaraktan bu dosyayoluna kopyalarsanız pc niz açıldığı zaman bu .ahk otomatik olarak çalıştırılır.

# Ubuntu Users

Ubuntu users içinde windowsdaki tavsiyeler geçerlidir ide + docker sistemi aynı çalışacaktır.

## Docker komutları:

### 2. Build Docker Images

Bu komutu, önbelleğe alınmış bir katmanın sorunlara neden olduğunu düşünüyorsanız kullanabilirsiniz (örneğin, bağımlılıkların düzgün güncellenmemesi).
Ya da Dockerfile içinde yaptığınız değişikliklerin (apt-get veya benzer komutlar gibi) Docker’ın katman önbelleği tarafından tanınamayabileceğini düşünüyorsanız kullanabilirsiniz:

```docker-compose build --no-cache```

Uygulamanızda veya Dockerfile’da değişiklik yaptıysanız ve görüntüyü yeniden oluşturup konteynerları başlatmak istiyorsanız, bu komutu çalıştırmanız yeterlidir.

```docker-compose up -d --build``` 

### 3. Start Docker Containers:
```docker-compose up```, or ```docker-compose up -d``` 

### 4. Attach Visual Studio Code to Docker Container

1.Wsl de VSCode u aç.

2.Docker extension panel'e gel.

3.Çalışan container'ı bul

4.container a sağ tıkla ve **Attach Visual Studio Code**.

Bu adımlar Docker container'ı içindeki dosya sistemine bağlı bir Vsiual Studio Code açar. Yaptığınız uygulamaları doğrudan container içerisinde geliştirebilirsiniz.