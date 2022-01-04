package org.class_sorter.model;


import java.io.File;
import java.io.FileNotFoundException;
import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;

public class Factory {

    public static List<Camper> createCampers(File pathname) throws FileNotFoundException {
        List<Camper> campers = new ArrayList<>();
        Scanner sc = new Scanner(pathname);
        sc.useDelimiter(",|\\r\\n|\\t");
        while (sc.hasNext()) {
            String lastName = sc.next();
            String firstName = sc.next();
            int age = sc.nextInt();
            String cabin = sc.next();
            String canShootString = sc.next();
            boolean canShoot = canShootString.equals("True") || canShootString.equals("true") || canShootString.equals("TRUE");
            List<String> prefs = new ArrayList<>();
            prefs.add(sc.next());
            prefs.add(sc.next());
            prefs.add(sc.next());
            prefs.add(sc.next());
            /*prefs.add(sc.next());
            prefs.add(sc.next());*/
            campers.add(new CamperImpl(firstName, lastName, age, cabin, canShoot, prefs));
        }
        return campers;
    }

    public static List<Class_> createClasses(File pathname) throws FileNotFoundException {
        List<Class_> classes = new ArrayList<>();
        Scanner sc = new Scanner(pathname);
        sc.useDelimiter(",|\\r\\n");
        while (sc.hasNext()) {
            String name = sc.next();
            int A_Capacity = sc.nextInt();
            int B_Capacity = sc.nextInt();
            int C_Capacity = sc.nextInt();
            int D_Capacity = sc.nextInt();
            String requiresShootingFormString = sc.next();
            boolean requiresShootingForm = requiresShootingFormString.equals("True") || requiresShootingFormString.equals("true") || requiresShootingFormString.equals("TRUE");
            classes.add(new ClassImpl(name, A_Capacity,B_Capacity,C_Capacity,D_Capacity, requiresShootingForm));
        }
        return classes;
    }
}
