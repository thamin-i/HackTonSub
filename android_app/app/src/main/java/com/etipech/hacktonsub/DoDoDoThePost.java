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
//        doThePost(email, restaurant, mark, ticket);
    }

    void doThePost(String email, String restaurant, String mark, String ticket){
        System.out.println("TOutoyuzd");
        try {
            URL url = new URL("http://10.15.192.243:4242");
            HttpURLConnection conn = (HttpURLConnection) url.openConnection();
            //HttpsURLConnection conn = (HttpsURLConnection) url.openConnection();
            conn.setReadTimeout(10000);
            conn.setConnectTimeout(15000);
            conn.setRequestMethod("POST");
            conn.setDoInput(true);
            conn.setDoOutput(true);

            Uri.Builder builder = new Uri.Builder()
                    .appendQueryParameter("email", email)
                    .appendQueryParameter("restaurant", restaurant)
                    .appendQueryParameter("mark", mark)
                    .appendQueryParameter("ticket", ticket);

            Log.e("DEBUG", "email=" + email + "&restaurant= " + restaurant + "&mark=" + mark + "&ticket=" + ticket.toString());

            String query = builder.build().getEncodedQuery();

            OutputStream os = conn.getOutputStream();
            BufferedWriter writer = new BufferedWriter(new OutputStreamWriter(os, "UTF-8"));
            writer.write(query);
            writer.flush();
            writer.close();
            os.close();

            conn.connect();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

}
