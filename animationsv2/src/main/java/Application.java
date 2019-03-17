import javax.swing.*;
import java.awt.*;

import com.google.auth.oauth2.GoogleCredentials;
import com.google.firebase.FirebaseApp;
import com.google.firebase.FirebaseOptions;
import com.google.firebase.database.*;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.FileInputStream;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;

public class Application  extends JFrame {
    boolean is_running = false;
    DataSnapshot data = null;


    private Application () {
        getDb();
    }

    private void getDb() {
        try {
            FileInputStream serviceAccount = new FileInputStream("C:/Users/stran/Documents/PROGRAMMING/Hackathons/Unihack 2019/animationsv2/src/main/resources/serviceAccountCredentials.json");

            FirebaseOptions options = new FirebaseOptions.Builder()
                    .setCredentials(GoogleCredentials.fromStream(serviceAccount))
                    .setDatabaseUrl("https://unihack19-6452a.firebaseio.com/")
                    .build();

            FirebaseApp.initializeApp(options);

            DatabaseReference ref = FirebaseDatabase.getInstance()
                    .getReference("/traffic/live");
            ref.addListenerForSingleValueEvent(new ValueEventListener() {
                @Override
                public void onDataChange(DataSnapshot dataSnapshot) {
                    data = dataSnapshot;
                    InitUI();
                }

                @Override
                public void onCancelled(DatabaseError error) {
                }
            });
        } catch (Exception e) {
            e.printStackTrace();
        }

    }

    private void InitUI(){
        if (!is_running) {
            add(new Simulator(data));

            setExtendedState(JFrame.MAXIMIZED_BOTH);
            setTitle("Traffic Simulator");
            setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);

            is_running = true;
        }
    }

    public static void main(String[] args) {
        EventQueue.invokeLater(() -> {
            Application app = new Application();
            app.setVisible(true);
        });
    }

    private static JSONObject parseJSONFile(String filename) throws JSONException, IOException {
        String content = new String(Files.readAllBytes(Paths.get(filename)));
        return new JSONObject(content);
    }
}
