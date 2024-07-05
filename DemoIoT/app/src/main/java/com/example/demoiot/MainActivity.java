package com.example.demoiot;

import android.os.Bundle;
import android.util.Log;
import android.widget.TextView;

import androidx.activity.EdgeToEdge;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.graphics.Insets;
import androidx.core.view.ViewCompat;
import androidx.core.view.WindowInsetsCompat;

import com.github.angads25.toggle.interfaces.OnToggledListener;
import com.github.angads25.toggle.model.ToggleableView;
import com.github.angads25.toggle.widget.LabeledSwitch;

import org.eclipse.paho.client.mqttv3.IMqttDeliveryToken;
import org.eclipse.paho.client.mqttv3.MqttCallbackExtended;
import org.eclipse.paho.client.mqttv3.MqttException;
import org.eclipse.paho.client.mqttv3.MqttMessage;

import java.nio.charset.Charset;

public class MainActivity extends AppCompatActivity {
    MQTTHelper mqttHelper;
    TextView txtTemp, txtHumi;
    LabeledSwitch btnLED, btnPUMP;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        EdgeToEdge.enable(this);
        setContentView(R.layout.activity_main);

        txtTemp = findViewById(R.id.txtTemperature);
        txtHumi = findViewById(R.id.txtHumidity);
        btnLED = findViewById(R.id.btnLED);
        btnPUMP = findViewById(R.id.btnPUMP);

        btnLED.setOnToggledListener(new OnToggledListener() {
            @Override
            public void onSwitched(ToggleableView toggleableView, boolean isOn) {
//                if(isOn == true){
//                    sendDataMQTT("tuong96/feeds/nutnhan1", "1");
//                }else{
//                    sendDataMQTT("tuong96/feeds/nutnhan1", "0");
//                }
                sendDataMQTT("group114/feeds/button1/V1", "1");
            }
        });

        btnPUMP.setOnToggledListener(new OnToggledListener() {
            @Override
            public void onSwitched(ToggleableView toggleableView, boolean isOn) {
//                if(isOn == true){
//                    sendDataMQTT("tuong96/feeds/nutnhan2", "1");
//                }else{
//                    sendDataMQTT("tuong96/feeds/nutnhan2", "0");
//                }
                sendDataMQTT("group114/feeds/button2/V1", "1");
            }
        });

        startMQTT();
        //ViewCompat.setOnApplyWindowInsetsListener(findViewById(R.id.main), (v, insets) -> {
        //    Insets systemBars = insets.getInsets(WindowInsetsCompat.Type.systemBars());
        //    v.setPadding(systemBars.left, systemBars.top, systemBars.right, systemBars.bottom);
        //    return insets;
        //});
    }

    public void sendDataMQTT(String topic, String value){
        MqttMessage msg = new MqttMessage();
        msg.setId(1234);
        msg.setQos(0);
        msg.setRetained(false);

        byte[] b = value.getBytes(Charset.forName("UTF-8"));
        msg.setPayload(b);

        try {
            mqttHelper.mqttAndroidClient.publish(topic, msg);
        }catch (MqttException e){
        }
    }
    public void startMQTT() {
        mqttHelper = new MQTTHelper(this);
        mqttHelper.setCallback(new MqttCallbackExtended() {
            @Override
            public void connectComplete(boolean reconnect, String serverURI) {

            }

            @Override
            public void connectionLost(Throwable cause) {

            }

            @Override
            public void messageArrived(String topic, MqttMessage message) throws Exception {
                Log.d("TEST", topic + "***" + message.toString());
                switch (topic){
                    case "group114/feeds/temp/V1":
                        txtTemp.setText(message.toString() + "°C");
                        break;
                    case "group114/feeds/moi/V1":
                        Log.d("TEST MOI", topic + "***" + message.toString());
                        txtHumi.setText(message.toString() + "%");
                        break;
                    default:
                        break;
                }
//                if(topic.contains("cambien1")){
//                    txtTemp.setText(message.toString() + "°C");
//                }else if(topic.contains("cambien2")){
//                    txtHumi.setText(message.toString() + "%");
//                }else if(topic.contains("nutnhan1")){
//                    if(message.toString().equals("1")){
//                        btnLED.setOn(true);
//                    }else{
//                        btnLED.setOn(false);
//                    }
//                }else if(topic.contains("nutnhan2")){
//                    if(message.toString().equals("1")){
//                        btnPUMP.setOn(true);
//                    }else{
//                        btnPUMP.setOn(false);
//                    }
//                }else if(topic.contains("group114/feeds/temp/V1")) {
//                    txtTemp.setText(message.toString() + "°C");
//                }
            }

            @Override
            public void deliveryComplete(IMqttDeliveryToken token) {

            }
        });
    }
}