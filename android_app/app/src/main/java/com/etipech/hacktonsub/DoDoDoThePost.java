package com.etipech.hacktonsub;

import android.net.Uri;
import android.os.Bundle;
import android.support.design.widget.FloatingActionButton;
import android.support.design.widget.Snackbar;
import android.support.v7.app.AppCompatActivity;
import android.support.v7.widget.Toolbar;
import android.util.Log;
import android.view.View;

import java.io.BufferedWriter;
import java.io.OutputStream;
import java.io.OutputStreamWriter;
import java.net.HttpURLConnection;
import java.net.URL;

public class DoDoDoThePost extends AppCompatActivity {

    NetworkAsyncTask nwAsync;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_do_do_do_the_post);
        Toolbar toolbar = (Toolbar) findViewById(R.id.toolbar);
        setSupportActionBar(toolbar);

        nwAsync = new NetworkAsyncTask();
        Bundle b = getIntent().getExtras();
        String email = b.getString("email");
        String restaurant = b.getString("restaurant");
        String mark = b.getString("mark");
        String ticket = b.getString("ticket");

        System.out.println(email);
        System.out.println(restaurant);
        System.out.println(mark);
        System.out.println(ticket);
        FloatingActionButton fab = (FloatingActionButton) findViewById(R.id.fab);
        fab.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Snackbar.make(view, "Replace with your own action", Snackbar.LENGTH_LONG)
                        .setAction("Action", null).show();
            }
        });

        nwAsync.execute(email, restaurant, mark, ticket);
    }
}
