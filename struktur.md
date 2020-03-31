# paper

## fragen

- aufteilung?
  - gliederung?
- aufbau wie in buch anhand von transaktionsstruktur?
- sprache: englisch oder deutsch?



## gliederung

### einleitung
- was eine transaktion (wortherkunft etc.), 
- ueberleitung kontext in ethereum: rolle von transaktionen
 
### ueberblick
- struktur einer transaktion: grober ueberblick

### technisches

jannes
- wie funktioniert die serialisierung: network-serialization, recursive length prefix
- big endian-integers

### nonces

jannes
- erklaerung, rolle in eth
- technische problemstellungen

### gas

ture
- erklaerung, zweck: halting problem
- entwicklung gas preises, problemstellung fuer das netzwerk, preisspruenge und auswirkungen

### receipt
ture

- how do addresses work in eth, private key mechanism
- no validation

### transaction value and data
jannes

- erklaerung value und data
- erklaerung aller 4 kombinationen von value und data
- contract creation

### signature
ture

- erklaerung von digitalen signaturen im allgemeinen: DSA und ECDSA
- rolle in ethereum, bezug auf erklaerung von addressen und private key verschluesselung
- offline signing 
- multiple signature transactions

### transaction propagation

jannes
- storage on blockchain: mining, etc.

### security

TODO: feingliederung

1. Einleitung
2. Struktur und technische Umsetzung einer Transaktion
    1. Komponenten einer Transaktion
    2. Serialisierung
3. Komponenten im Detail
    1. Nonces
    2. Transaktionsgas
    3. Value und Data
4. Transaktionsabwicklung
    1. Statemachine
    2. Propagation und Aufzeichnung in der Blockchain
    3. Multisignatur-Transaktionen

5. Digitale Signaturen