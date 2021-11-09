package org.class_sorter.view;

import javafx.geometry.Insets;
import javafx.scene.Parent;
import javafx.scene.layout.GridPane;
import javafx.scene.text.Font;
import javafx.scene.text.FontWeight;
import javafx.scene.text.Text;
import org.class_sorter.controller.Controller;
import org.class_sorter.model.Model;
import org.class_sorter.model.ModelObserver;

public class View implements FXComponent, ModelObserver {
    private Controller controller;
    private Model model;

    public View(Controller controller, Model model) {
        if (controller == null) {
            throw new IllegalArgumentException();
        }
        this.controller = controller;
        this.model = model;
    }

    @Override
    public void update(Model model) {
        render();
    }

    @Override
    public Parent render() {
        GridPane grid = new GridPane();

        grid.setHgap(10);
        grid.setVgap(10);
        grid.setPadding(new Insets(0, 10, 0, 10));


        for (int i = 0; i < model.getCampers().size(); i++) {
            Text title = new Text(model.getCampers().get(i).getFirstName() + " " + model.getCampers().get(i).getLastName());
            grid.add(title,0,i);
        }
        return grid;
    }
}
