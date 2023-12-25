## Compile and push CPUInfoReader.java

```bash
javac CPUInfoReader.java
adb push CPUInfoReader.class /sdcard/
adb shell dalvikvm -cp /sdcard/ com.example.CPUInfoReader
```
