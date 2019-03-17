import com.google.firebase.database.DataSnapshot;

import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;

public class Simulator extends JPanel implements ActionListener {
    private final int DELAY = 5;
    private DataSnapshot events;
    private int ms_since_start = 0;
    private int current_tick = 0;
    private HashMap<Integer, ArrayList<Integer>> light_configs = new HashMap<>();
    private ArrayList<ArrayList<Car>> lanes = new ArrayList<>();

    private ArrayList<Car> exiting_cars = new ArrayList<>();
    private int lights = 0;


    Simulator(DataSnapshot events) {
        this.events = events;
        light_configs.put(0, new ArrayList<>(Arrays.asList(1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0)));
        light_configs.put(1, new ArrayList<>(Arrays.asList(0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0)));
        light_configs.put(2, new ArrayList<>(Arrays.asList(0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0)));
        light_configs.put(3, new ArrayList<>(Arrays.asList(0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1)));
        light_configs.put(4, new ArrayList<>(Arrays.asList(1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0)));
        light_configs.put(5, new ArrayList<>(Arrays.asList(0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0)));

        lanes.add(new ArrayList<>());
        lanes.add(new ArrayList<>());
        lanes.add(new ArrayList<>());
        lanes.add(new ArrayList<>());
        lanes.add(new ArrayList<>());
        lanes.add(new ArrayList<>());
        lanes.add(new ArrayList<>());
        lanes.add(new ArrayList<>());
        lanes.add(new ArrayList<>());
        lanes.add(new ArrayList<>());
        lanes.add(new ArrayList<>());
        lanes.add(new ArrayList<>());

        initSim();
    }

    private void initSim() {
        setFocusable(true);
        setBackground(Color.WHITE);
        Timer timer = new Timer(DELAY, this);
        timer.start();
    }

    @Override
    public void actionPerformed(ActionEvent e) {
        if (ms_since_start % 1000 == 0) {
            updateMovement();
            current_tick += 1;
        }
        updateExitAnimations();
        ms_since_start += 5;
        repaint();
    }

    private void updateExitAnimations() {

        for (Car car : exiting_cars) {
            car.update_exit_pos(ms_since_start);
            if (car.has_exited()) {
                exiting_cars.remove(car);
            }
        }
    }

    @Override
    public void paintComponent(Graphics g) {
        super.paintComponent(g);
        drawComponents(g);
        Toolkit.getDefaultToolkit().sync();
    }

    private void updateMovement() {
        // Trawl through the JSON to find new cars on this tick and new lights on this tick
        DataSnapshot event = events.child(Integer.toString(current_tick));

        System.out.println(event.getValue());
        boolean has_cars = event.hasChild("cars");
        if (has_cars) {
            for (DataSnapshot car : event.child("cars").getChildren()) {
                int lane = car.child("0").getValue(Integer.class);
                int turn_direction = car.child("1").getValue(Integer.class);
                lanes.get(lane).add(new Car(lane, turn_direction));
            }
        }

        // Get current light config
        int new_lights = event.child("light_config").getValue(Integer.class);

        // Get lanes where cars can move fwd and pop them
        for (int lane=0; lane<12; lane++) {
            boolean moveable = (light_configs.get(lights).get(lane) * light_configs.get(new_lights).get(lane)) == 1;

            if (moveable && !lanes.get(lane).isEmpty()) {
                exiting_cars.add(lanes.get(lane).get(0));
                lanes.get(lane).remove(0);
            }
        }

        // Update the lights
        lights = new_lights;

        // Update where current remaining cars are
        for (int lane_num = 0; lane_num < lanes.size(); lane_num++) {
            ArrayList<Car> car_list = lanes.get(lane_num);
            for (int index = 0; index < car_list.size(); index++) {
                Car car = car_list.get(index);
                car.update_pos(index, lane_num);
            }
        }


        System.out.println("Light config: " + lights + " cars: " + lanes);
    }

    private void drawComponents(Graphics g) {
        Graphics2D g2d = (Graphics2D) g;

        for (int lane_num = 0; lane_num < lanes.size(); lane_num++) {
            ArrayList<Car> car_list = lanes.get(lane_num);
            for (int index = 0; index < car_list.size(); index++) {
                Car car = lanes.get(lane_num).get(index);
                g2d.drawImage(car.getImage(), car.getX(), car.getY(), this);
            }
        }
    }
}
