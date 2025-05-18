pkgname=pdwmbar-bin
pkgver=1.0
pkgrel=1
pkgdesc='A simple dwmbar'
arch=('x86_64')
source=("main.bin")
sha256sums=('50b5609880c3db2cd96ee1285c65e89f0a0b76099f46227e92962351f968c763')
 
package() {
    install -Dm755 "$srcdir/main.bin" "$pkgdir/usr/bin/${pkgname%-bin}"
}
