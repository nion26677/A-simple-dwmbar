pkgname=pdwmbar-bin
pkgver=1.0
pkgrel=1
pkgdesc='A simple dwmbar'
arch=('x86_64')
source=("main.bin")
sha256sums=('52915f3a3596b4730e9299b785103cd60c57e47673aebbffdfc10b9e06c5e9b8')
 
package() {
    install -Dm755 "$srcdir/main.bin" "$pkgdir/usr/bin/${pkgname%-bin}"
}
