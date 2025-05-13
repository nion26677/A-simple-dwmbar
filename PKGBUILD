pkgname=pdwmbar-bin
pkgver=1.0
pkgrel=1
pkgdesc='A simple dwmbar'
arch=('x86_64')
source=("main.bin")
sha256sums=('')
 
package() {
    install -Dm755 "$srcdir/main.bin" "$pkgdir/usr/bin/${pkgname%-bin}"
}
