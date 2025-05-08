pkgname=pdwmbar-bin
pkgver=1.0
pkgrel=1
pkgdesc='A simple dwmbar'
arch=('x86_64')
source=("main.bin")
sha256sums=('0e50b492623ca7f7d92091d704ae543a2498b00906355e9ec7e425180b179dd3')
 
package() {
    install -Dm755 "$srcdir/main.bin" "$pkgdir/usr/bin/${pkgname%-bin}"
}
