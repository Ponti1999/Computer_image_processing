<h1 align="center"> Eye Blink Fatigue Detection Project </h1> <br>

<p align="center">
  A fatigue detection program using a webcam to monitor eye blinks and estimate user fatigue levels. Built with Python, OpenCV, and Tkinter.
</p>

## English Version

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
## Table of Contents

- [English Version](#english-version)
  - [Introduction](#introduction)
  - [Industry Use Cases](#industry-use-cases)
  - [Features](#features)
  - [Technologies](#technologies)
  - [Implementation Details](#implementation-details)
  - [First Version](#first-version)
  - [First Blink Detection Version](#first-blink-detection-version)
  - [First Version Issues](#first-version-issues)
  - [Second Version Improvements](#second-version-improvements)
  - [Adding Alerts and Counters](#adding-alerts-and-counters)
  - [Testing Other Approaches](#testing-other-approaches)
  - [Debugging and UI Updates](#debugging-and-ui-updates)
- [Future Improvements](#future-improvements)
- [References](#references)
- [Magyar Verzió](#magyar-verzió)
  - [Bevezetés](#bevezetés)
  - [Ipari Felhasználási Esetek](#ipari-felhasználási-esetek)
  - [Jellemzők](#jellemzők)
  - [Technológiák](#technológiák)
  - [Megvalósítási Részletek](#megvalósítási-részletek)
  - [Első Verzió](#első-verzió)
  - [Első Pislogás Érzékelő Verzió](#első-pislogás-érzékelő-verzió)
  - [Első Verzió Problémái](#első-verzió-problémái)
  - [Második Verzió Javításai](#második-verzió-javításai)
  - [Riasztások és Számlálók Hozzáadása](#riasztások-és-számlálók-hozzáadása)
  - [Más Megközelítések Tesztelése](#más-megközelítések-tesztelése)
  - [Hibakeresés és UI Frissítések](#hibakeresés-és-ui-frissítések)
- [Jövőbeli Fejlesztések](#jövőbeli-fejlesztések)
- [Hivatkozások](#hivatkozások)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

### Introduction

This project aims to create a practical program that can monitor and assess user fatigue based on eye blinking patterns detected via a webcam. By calculating blink frequency and open-eye ratios, the program evaluates fatigue levels, which can be crucial for productivity and safety in work or personal environments.

As a student and employee who spends a significant amount of time in front of a computer, I noticed the importance of addressing fatigue before it negatively impacts productivity. This software offers a potential solution by tracking eye movements and providing feedback to the user.

The most common use today is in the automotive industry, where the driver's fatigue level is monitored. Blink frequency is generally around 12 blinks per minute on average [1].

### Industry Use Cases
The system could be applied in various environments, such as transportation or personal workspaces. In vehicles, especially in transportation or logistics, this system helps monitor driver alertness by detecting eye blinks and other signs of fatigue. Systems like this are typically installed on the windshield of vehicles, connected to a company’s system through cloud-based alerts for external evaluations [2].

### Features

Some of the key features of this project include:

- Real-time eye blink detection using a webcam.
- Fatigue assessment based on blink frequency (average of 12 blinks per minute [1]).
- Basic user interface (UI) built with Tkinter for displaying blink counts and fatigue indicators.
- Potential for further development into more sophisticated fatigue monitoring systems.

### Technologies

This project utilizes the following technologies:

- **Languages**: Python 3
- **Libraries**:
  - OpenCV for facial and eye detection.
  - Tkinter for creating the user interface.
- **Algorithms**: Haar Cascade for face and eye detection, contour-based analysis for blink detection.

### Implementation Details

The software captures real-time video through the device's webcam and uses OpenCV to detect facial landmarks. Specifically, it tracks the eyes and calculates eyelid distance to detect blinks. This information is then used to monitor blink frequency, which indicates user fatigue levels.

### First Version

<p align="center">
  <img src="./img/facemash.png" alt="FaceMashDetector" width="400">
</p>

1. **Face and Eye Detection**:
   - Implemented using Haar Cascade classifiers from OpenCV.
   - Facial landmarks around the eyes are located to calculate the distance between eyelids.

<p align="center">
  <img src="./img/face_points.png" alt="Face orientation points" width="400">
</p>

### First Blink Detection Version

2. **Blink Detection**:
   - The distance between the upper and lower eyelids is measured to detect blinks. When the distance decreases below a threshold, a blink is registered. This method is based on standard eyelid movements observed in fatigue monitoring research [2].

<p align="center">
  <img src="./img/blinking_charact.png" alt="Blink detection characterization" width="400">
</p>

   - A historical data array stores recent blink events, and if the blink frequency falls below the average threshold, the program triggers a fatigue alert.

<p align="center">
  <img src="./img/eyes_crossed.png" alt="Eyes crossed for blink detection" width="400">
</p>

3. **Fatigue Monitoring**:
   - The program counts the number of blinks per minute and compares it with the standard 12 blinks/minute threshold to assess fatigue [1].
   - If the blink count is too low, an alert is triggered, indicating potential user fatigue.

### First Version Issues
Despite getting valid results, three issues were noticed:
- **Fast blinks**: The system rarely detected quick blinks.
- **Winking**: It falsely detected minimal eye closures (such as winking) as blinks.
- **Camera movement**: The blink threshold got stuck and the system stopped detecting when the camera moved back and forth.

### Second Version Improvements

In the second version, the following adjustments were made:

- Measured eyelid areas instead of just distances, using contour calculations for more accuracy.
- Blink events are now detected more reliably, even for fast blinks or winking, and the system adapts to camera movements dynamically.

<p align="center">
  <img src="./img/left_plot.png" alt="Left eye blink detection plot" width="400">
</p>

- **1**: The historical data and threshold show clear downward spikes, indicating valid blink detections.
- **2**: When the camera moves closer to the subject, the system adjusts to the larger eye area, ensuring proper detection.
- **3**: Moving away from the camera previously caused detection issues, but now the system adjusts by dynamically managing the historical data.

<p align="center">
  <img src="./img/left_eye_imp.png" alt="Left eye improved plot" width="400">
</p>

This improved version successfully handles exceptions such as:
- Closer or further camera movements.
- Quick blinks and winks, which are correctly detected or ignored, respectively.

### Adding Alerts and Counters

In the final step, a counter and a time function were added to monitor whether the system detects at least 12 blinks in 60 seconds. If not, an alert is triggered. The alert, in this case, is a predefined MP3 file that plays when the user hasn't blinked enough.

### Testing Other Approaches

Two other approaches were also tested during the implementation process. One of them involved using a trained model for eye detection, achieving around 70% accuracy. However, I couldn't extract enough useful information about eye closure from this detection method.

The second approach was similar to the first, where I tried training the model myself. However, due to a lack of labeled data, I was unable to perform effective pre-training. Real-time learning proved ineffective, as it required too much time to achieve limited results.

### Debugging and UI Updates

In this version, I added real-time logging for data analysis. The system logs blink events for later graph analysis, and the UI displays the blink frequency dynamically.

## Future Improvements

Here are some potential areas for further development:

1. **Blink Duration Analysis**: Include the length of time each blink lasts to provide more accurate fatigue assessments.

2. **Yawning Detection**: Integrate additional facial gesture analysis to detect yawns, enhancing fatigue monitoring accuracy.

3. **Environment-based Adjustments**: Analyze how blinking behavior changes based on time of day or environmental factors.

4. **Eye Openness Classification**: Implement a system that classifies eye openness levels to identify varying states of fatigue.

5. **Multi-user Support**: Enable the system to track fatigue for multiple users simultaneously by detecting different faces in the frame.

## References

1. K.-A. Kwon, R. J. Shipley, M. Edirisinghe, D. G. Ezra, G. Rose, S. M. Best, and R. E. Cameron, "High-speed camera characterization of voluntary eye blinking kinematics," Journal of the Royal Society Interface, vol. 10, no. 85, p. 20130227, 2013. [Link](https://doi.org/10.1098/rsif.2013.0227)

2. L. Oliveira, J. S. Cardoso, A. Lourenço, and C. Ahlström, "Driver drowsiness detection: a comparison between intrusive and non-intrusive signal acquisition methods," 2018 7th European Workshop on Visual Information Processing (EUVIP), Tampere, Finland, 2018. [Link](https://ieeexplore.ieee.org/document/8611704)

</br>
</br>

--------------------------------

</br>
</br>

<h1 align="center"> Pislogás Alapú Fáradtság Érzékelő Projekt </h1> <br>

<p align="center">
  Egy fáradtságérzékelő program, amely webkamerát használ a pislogások figyelésére és a felhasználó fáradtsági szintjének becslésére. Python, OpenCV és Tkinter felhasználásával készült.
</p>

## Magyar Verzió

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
## Tartalomjegyzék (Magyar)

- [English Version](#english-version)
- [Table of Contents](#table-of-contents)
  - [Introduction](#introduction)
  - [Industry Use Cases](#industry-use-cases)
  - [Features](#features)
  - [Technologies](#technologies)
  - [Implementation Details](#implementation-details)
  - [First Version](#first-version)
  - [First Blink Detection Version](#first-blink-detection-version)
  - [First Version Issues](#first-version-issues)
  - [Second Version Improvements](#second-version-improvements)
  - [Adding Alerts and Counters](#adding-alerts-and-counters)
  - [Testing Other Approaches](#testing-other-approaches)
  - [Debugging and UI Updates](#debugging-and-ui-updates)
- [Future Improvements](#future-improvements)
- [References](#references)
- [Magyar Verzió](#magyar-verzió)
- [Tartalomjegyzék (Magyar)](#tartalomjegyzék-magyar)
  - [Bevezetés](#bevezetés)
  - [Ipari Felhasználási Esetek](#ipari-felhasználási-esetek)
  - [Jellemzők](#jellemzők)
  - [Technológiák](#technológiák)
  - [Megvalósítási Részletek](#megvalósítási-részletek)
  - [Első Verzió](#első-verzió)
  - [Első Pislogás Érzékelő Verzió](#első-pislogás-érzékelő-verzió)
  - [Első Verzió Problémái](#első-verzió-problémái)
  - [Második Verzió Javításai](#második-verzió-javításai)
  - [Riasztások és Számlálók Hozzáadása](#riasztások-és-számlálók-hozzáadása)
  - [Más Megközelítések Tesztelése](#más-megközelítések-tesztelése)
  - [Hibakeresés és UI Frissítések](#hibakeresés-és-ui-frissítések)
- [Jövőbeli Fejlesztések](#jövőbeli-fejlesztések)
- [Hivatkozások](#hivatkozások)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

### Bevezetés

Ez a projekt egy olyan program létrehozását célozza, amely a webkamera segítségével képes monitorozni és értékelni a felhasználó fáradtságát a pislogási minták alapján. A pislogások gyakoriságát és a nyitott szemek arányát figyelve a program fáradtsági szinteket értékel, amelyek a produktivitás és a biztonság szempontjából elengedhetetlenek lehetnek munka vagy személyes használat során.

Diákként és alkalmazottként, aki hosszú időt tölt a számítógép előtt, fontosnak tartom, hogy foglalkozzunk a fáradtsággal, mielőtt az negatívan befolyásolná a produktivitást. Ez a szoftver egy lehetséges megoldást kínál a szemmozgások nyomon követésére és a felhasználónak adott visszajelzésekre.

A leggyakoribb felhasználás ma az autóiparban van, ahol a sofőr fáradtsági szintjét figyelik. A pislogások gyakorisága általában körülbelül 12 pislogás percenként [1].

### Ipari Felhasználási Esetek
A rendszert különféle környezetekben lehetne alkalmazni, például a közlekedésben vagy a munkahelyeken. A járművekben, különösen a közlekedési vagy logisztikai szektorban, ez a rendszer a sofőr éberségét figyeli a pislogások és egyéb fáradtsági jelek alapján. Ilyen rendszerek általában a jármű szélvédőjén találhatók, és a felhőn keresztül kapcsolódnak a cég rendszeréhez külső kiértékelés céljából [2].

### Jellemzők

A projekt néhány fő jellemzője a következő:

- Valós idejű pislogás érzékelés webkamera segítségével.
- Fáradtság értékelés a pislogási gyakoriság alapján (átlagosan 12 pislogás percenként [1]).
- Alap felhasználói felület (UI), amely a pislogások számát és a fáradtsági jelzőket jeleníti meg.
- Lehetőség további fejlesztésekre, hogy egy kifinomultabb fáradtságfigyelő rendszer alakuljon ki.

### Technológiák

A projekt a következő technológiákat használja:

- **Programnyelvek**: Python 3
- **Könyvtárak**:
  - OpenCV az arc- és szemdetektáláshoz.
  - Tkinter a felhasználói felület létrehozásához.
- **Algoritmusok**: Haar Cascade az arc- és szemdetektáláshoz, kontúralapú elemzés a pislogások érzékelésére.

### Megvalósítási Részletek

A szoftver valós idejű videót rögzít az eszköz webkameráján keresztül, és az OpenCV-t használja az arcjelzők érzékelésére. Kifejezetten a szemeket követi, és a szemhéjak közötti távolságot számítja ki a pislogások érzékeléséhez. Ez az információ a pislogási gyakoriság monitorozására szolgál, ami a felhasználó fáradtsági szintjeit jelzi.

### Első Verzió

<p align="center">
  <img src="./img/facemash.png" alt="FaceMashDetector" width="400">
</p>

1. **Arc- és Szemérzékelés**:
   - Az OpenCV-ből származó Haar Cascade osztályozókat alkalmazták.
   - Az arc körüli arcrészletek alapján számítja ki a szemhéjak közötti távolságot.

<p align="center">
  <img src="./img/face_points.png" alt="Arc tájékozódási pontok" width="400">
</p>

### Első Pislogás Érzékelő Verzió

2. **Pislogás Érzékelés**:
   - A felső és alsó szemhéjak közötti távolságot mérik, hogy érzékeljék a pislogást. Amikor a távolság egy küszöbérték alá csökken, egy pislogást regisztrálnak. Ez a módszer a fáradtságfigyelő kutatások során megfigyelt szemhéjmozgásokon alapul [2].

<p align="center">
  <img src="./img/blinking_charact.png" alt="Pislogás detektálás jellemzése" width="400">
</p>

   - Egy történeti adatsor tárolja a legutóbbi pislogásokat, és ha a pislogási gyakoriság az átlagos küszöbérték alá esik, a program fáradtsági riasztást vált ki.

<p align="center">
  <img src="./img/eyes_crossed.png" alt="Pislogás érzékeléshez összekulcsolt szemek" width="400">
</p>

3. **Fáradtságfigyelés**:
   - A program megszámolja a pislogások számát percenként, és összehasonlítja az átlagos 12 pislogás/perc küszöbértékkel a fáradtság értékeléséhez [1].
   - Ha a pislogások száma túl alacsony, riasztást vált ki, amely potenciális fáradtságot jelez.

### Első Verzió Problémái
Bár érvényes eredményeket kaptunk, három problémát észleltünk:
- **Gyors pislogások**: A rendszer ritkán érzékelte a gyors pislogásokat.
- **Kacsintás**: Tévesen érzékelte a minimális szemcsukásokat (pl. kacsintást) pislogásnak.
- **Kamera mozgása**: A pislogási küszöb rögzült, és a rendszer nem érzékelt tovább, ha a kamera előre-hátra mozgott.

### Második Verzió Javításai

A második verzióban a következő módosításokat végezték el:

- A szemhéjak területét mérték a távolságok helyett, kontúrszámításokkal a pontosság érdekében.
- A pislogási eseményeket most megbízhatóbban érzékelik, még a gyors pislogásokat vagy kacsintásokat is, és a rendszer dinamikusan alkalmazkodik a kamera mozgásához.

<p align="center">
  <img src="./img/left_plot.png" alt="Bal szem pislogás érzékelési diagram" width="400">
</p>

- **1**: A történeti adatok és a küszöbértékek világosan mutatják a lefelé irányuló kiugrásokat, amelyek érvényes pislogásokat jeleznek.
- **2**: Amikor a kamera közelebb kerül a felhasználóhoz, a rendszer alkalmazkodik a nagyobb szemterülethez, biztosítva a megfelelő érzékelést.
- **3**: A kamerától való eltávolodás korábban érzékelési problémákat okozott, de most a rendszer dinamikusan kezeli a történeti adatokat.

<p align="center">
  <img src="./img/left_eye_imp.png" alt="Bal szem javított diagram" width="400">
</p>

Ez a javított verzió sikeresen kezeli az olyan kivételeket, mint:
- Közeledő vagy távolodó kamera mozgása.
- Gyors pislogások és kacsintások, amelyek helyesen érzékelhetők vagy figyelmen kívül hagyhatók.

### Riasztások és Számlálók Hozzáadása

A végső lépésként hozzáadtunk egy számlálót és egy időzítő függvényt, amely figyeli, hogy a rendszer 60 másodperc alatt legalább 12 pislogást észlel-e. Ha nem, riasztást vált ki. A riasztás ebben az esetben egy előre kiválasztott MP3 fájl lejátszása, amely akkor szólal meg, ha a felhasználó nem pislogott eleget.

### Más Megközelítések Tesztelése

Két másik megközelítést is kipróbáltunk a megvalósítás során. Az egyik egy betanított modell alapján való szemérzékelést alkalmazott, amely körülbelül 70%-os pontosságot ért el. Azonban nem sikerült elegendő hasznos információt kinyerni a szemcsukásról ebből a módszerből.

A második megközelítés hasonló volt az elsőhöz, ahol én magam próbáltam betanítani a modellt. Azonban címkézett adatok hiányában nem sikerült hatékony előre betanítást végrehajtani. A valós idejű tanulás nem bizonyult hasznosnak, mivel túl sok időre volt szükség a korlátozott eredmények eléréséhez.

### Hibakeresés és UI Frissítések

Ebben a verzióban hozzáadtam valós idejű naplózást az adatelemzéshez. A rendszer naplózza a pislogási eseményeket későbbi grafikon elemzés céljából, és a felhasználói felület dinamikusan jeleníti meg a pislogási gyakoriságot.

## Jövőbeli Fejlesztések

Néhány lehetséges továbbfejlesztési terület:

1. **Pislogás időtartamának elemzése**: A pislogások időtartamának figyelembevétele a fáradtság pontosabb értékelése érdekében.

2. **Ásítás észlelése**: További arckifejezések elemzése az ásítások észlelésére, javítva ezzel a fáradtság monitorozásának pontosságát.

3. **Környezeti beállítások**: A pislogási szokások elemzése a napszak vagy más környezeti tényezők figyelembevételével.

4. **Szemnyitás szintjének osztályozása**: Egy rendszer implementálása, amely osztályozza a szemnyitás szintjeit a különböző fáradtsági állapotok azonosítására.

5. **Többfelhasználós támogatás**: A rendszer lehetővé teheti, hogy több felhasználó fáradtságát egyszerre kövessék nyomon az arcok detektálásával.

## Hivatkozások

1. K.-A. Kwon, R. J. Shipley, M. Edirisinghe, D. G. Ezra, G. Rose, S. M. Best, and R. E. Cameron, "High-speed camera characterization of voluntary eye blinking kinematics," Journal of the Royal Society Interface, vol. 10, no. 85, p. 20130227, 2013. [Link](https://doi.org/10.1098/rsif.2013.0227)

2. L. Oliveira, J. S. Cardoso, A. Lourenço, and C. Ahlström, "Driver drowsiness detection: a comparison between intrusive and non-intrusive signal acquisition methods," 2018 7th European Workshop on Visual Information Processing (EUVIP), Tampere, Finland, 2018. [Link](https://ieeexplore.ieee.org/document/8611704)
