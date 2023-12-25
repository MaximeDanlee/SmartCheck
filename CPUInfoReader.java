import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.FileWriter;

public class CPUInfoReader {
    public static void main(String[] args) {
        try {
            Process process = Runtime.getRuntime().exec("cat sys/class/thermal/thermal_zone0/temp");
            BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream()));

            FileWriter writer = new FileWriter("temperature_output.txt");

            String line;
            while ((line = reader.readLine()) != null) {
                System.out.println(line);
                writer.write(line + "\n");
            }

            reader.close();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
