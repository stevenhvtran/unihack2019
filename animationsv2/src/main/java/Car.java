import javax.imageio.ImageIO;
import javax.swing.*;
import java.awt.*;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Arrays;

public class Car extends JComponent {
    private int x, y;
    private int height, width;
    private Image image;
    ArrayList<Integer> start_pos_x = new ArrayList<>(Arrays.asList(665, 625, 585, 1200, 1200, 1200, 505, 545, 585, 0, 0, 0));
    ArrayList<Integer> start_pos_y = new ArrayList<>(Arrays.asList(0, 0, 0, 665, 625, 585, 1200, 1200, 1200, 505, 545, 585));
    ArrayList<Integer> intersection_pos_x = new ArrayList<>(Arrays.asList(665, 625, 585, 700, 700, 700, 505, 545, 585, 470, 470, 470));
    ArrayList<Integer> intersection_pos_y = new ArrayList<>(Arrays.asList(470, 470, 470, 665, 625, 585, 700, 700, 700, 505, 545, 585));
    private boolean exited = false;
    private int turn_direction;
    ArrayList<ArrayList<Integer>> intersection_locations = new ArrayList<>();
    ArrayList<ArrayList<Integer>> goal_locations = new ArrayList<>();
    private int lane;

    Car(int lane, int turn_direction) {
        this.turn_direction = turn_direction;
        this.lane = lane;
        x = start_pos_x.get(lane);
        y = start_pos_y.get(lane);

        loadImage("car.png");
        width = image.getWidth(null);
        height = image.getHeight(null);

        intersection_locations.add(new ArrayList<>(Arrays.asList(665, 505)));
        intersection_locations.add(new ArrayList<>(Arrays.asList(665, 505)));
        intersection_locations.add(new ArrayList<>(Arrays.asList(625, 505)));
        intersection_locations.add(new ArrayList<>(Arrays.asList(585, 680)));

        intersection_locations.add(new ArrayList<>(Arrays.asList(650, 670)));
        intersection_locations.add(new ArrayList<>(Arrays.asList(600, 665)));
        intersection_locations.add(new ArrayList<>(Arrays.asList(600, 625)));
        intersection_locations.add(new ArrayList<>(Arrays.asList(650, 585)));

        intersection_locations.add(new ArrayList<>(Arrays.asList(505, 665)));
        intersection_locations.add(new ArrayList<>(Arrays.asList(505, 600)));
        intersection_locations.add(new ArrayList<>(Arrays.asList(545, 600)));
        intersection_locations.add(new ArrayList<>(Arrays.asList(585, 545)));

        intersection_locations.add(new ArrayList<>(Arrays.asList(505, 505)));
        intersection_locations.add(new ArrayList<>(Arrays.asList(550, 505)));
        intersection_locations.add(new ArrayList<>(Arrays.asList(550, 545)));
        intersection_locations.add(new ArrayList<>(Arrays.asList(625, 585)));

        goal_locations.add(new ArrayList<>(Arrays.asList(1200, 505)));
        goal_locations.add(new ArrayList<>(Arrays.asList(665, 1200)));
        goal_locations.add(new ArrayList<>(Arrays.asList(625, 1200)));
        goal_locations.add(new ArrayList<>(Arrays.asList(0, 625)));

        goal_locations.add(new ArrayList<>(Arrays.asList(665, 1200)));
        goal_locations.add(new ArrayList<>(Arrays.asList(0, 665)));
        goal_locations.add(new ArrayList<>(Arrays.asList(-30, 625)));
        goal_locations.add(new ArrayList<>(Arrays.asList(545, 0)));

        goal_locations.add(new ArrayList<>(Arrays.asList(0, 665)));
        goal_locations.add(new ArrayList<>(Arrays.asList(505, 0)));
        goal_locations.add(new ArrayList<>(Arrays.asList(545, 0)));
        goal_locations.add(new ArrayList<>(Arrays.asList(1200, 545)));

        goal_locations.add(new ArrayList<>(Arrays.asList(505, 0)));
        goal_locations.add(new ArrayList<>(Arrays.asList(1200, 505)));
        goal_locations.add(new ArrayList<>(Arrays.asList(1200, 545)));
        goal_locations.add(new ArrayList<>(Arrays.asList(6625, 1200));
        
    }

    public void update_pos(int index, int lane) {
        int road_num = lane / 3;
        if (road_num == 0) {
            y = intersection_pos_y.get(lane) - index * width;
        } else if (road_num == 1) {
            x = intersection_pos_x.get(lane) + index * width;
        } else if (road_num == 2) {
            y = intersection_pos_y.get(lane) + index * height;
        } else if (road_num == 3) {
            x = intersection_pos_x.get(lane) - index * width;
        }
    }

    private void loadImage(String imageName) {
        try {
            image = ImageIO.read(this.getClass().getResourceAsStream(imageName));
        } catch (IOException e) {
            System.out.println("Couldn't load image from: " + imageName);
        }
    }

    public int getX() { return x; }
    public int getY() { return y; }

    public int getWidth() { return width; }

    public int getHeight() { return height; }

    public Image getImage() { return image; }

    public Rectangle getBounds() {
        return new Rectangle(x, y, width, height);
    }

    public void move_towards_intersection() {
        int x_delta = 0;
        int y_delta = 0;
        int road_num = lane / 3;
        int n = road_num * 4 + turn_direction;
        if (road_num == 0) {
            y_delta =  intersection_locations.get(n).get(1) - intersection_pos_y.get(lane);
        } else if (road_num == 1) {
            x_delta = intersection_pos_x.get(lane) - intersection_locations.get(n).get(0);
        } else if (road_num == 2) {
            y_delta = intersection_pos_y.get(lane) - intersection_locations.get(n).get(1);
        } else if (road_num == 3) {
            x_delta = intersection_locations.get(n).get(0) - intersection_pos_x.get(lane);
        }
        return 
    }

    public void update_exit_pos(int ms_ticks) {

        int rounded_ticks = ms_ticks / 1000;
        if (rounded_ticks < 500) {
            // move towards intersection

        } else {
            // move towards exit
        }
    }

    public boolean has_exited() {
        return exited;
    }
}
