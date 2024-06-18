clear;
close all;

DATA = [10 20 30 40 50 60 70 80 90 100];

fprintf('Creating server socket for proxy...');
TCPIPServer = tcpserver('127.0.0.1', 6001);
fprintf(' CREATED\n');

while true
    if TCPIPServer.NumBytesAvailable ~= 0
        
        data = read(TCPIPServer, TCPIPServer.NumBytesAvailable, "string");
        fprintf('Message received by server: ');
        disp(data) 
        dataSplit = split(data , ["="," ",";",","]);
        msg = "";
        if dataSplit(1) == "GET"
            msg = "OK IND=";
            for i=3:(length(dataSplit)-1)
                if i == (length(dataSplit)-1)
                    msg = append(msg, dataSplit(i), " ");
                else
                    msg = append(msg, dataSplit(i), ",");
                end
            end
            a = "DATA=";
            msg = append(msg, a);
            for i=3:(length(dataSplit)-1)
                if i == (length(dataSplit)-1)
                    msg = append(msg, num2str(DATA(str2num(dataSplit(i))+1)), ";");
                else
                    msg = append(msg, num2str(DATA(str2num(dataSplit(i))+1)), ",");
                end
            end
            fprintf('Message sent by server: ');
            reply(TCPIPServer,msg);
        elseif dataSplit(1) == "SET"
            msg = "OK;";
            lenIndex = 3;
            a = "DATA";
            while dataSplit(lenIndex) ~= a
                lenIndex = lenIndex + 1;
            end
            for i=3: (lenIndex-1)
                DATA(str2num(dataSplit(i))+1) = str2num(dataSplit(lenIndex-2+i));
            end
            fprintf('Message sent by server: ');
            reply(TCPIPServer,msg);
            updatePrint(DATA);
        elseif dataSplit(1) == "RESET"
            if length(dataSplit) > 2
                for i = 1: 10
                    DATA(i) = str2num(dataSplit(3));
                end
            else
                b = "";
                for i = 1: 10
                    DATA(i) = b;
                end                
            end
            msg = "OK;";
            fprintf('Message sent by server: ');
            reply(TCPIPServer,msg);
            updatePrint(DATA);
        end      
    end
end

function reply(srv, packet)
    while (1) % try a few times, if you only try once you get an error saying client is not connected
        try
            disp(packet);
            srv.write(packet); % send reply to proxy        
            break;
        catch
            pause(0.01); % wait for some amount
        end
    end
end
function updatePrint(array)
    x0 = ['0    ',num2str(array(1))];
    x1 = ['1    ',num2str(array(2))];
    x2 = ['2    ',num2str(array(3))];
    x3 = ['3    ',num2str(array(4))];
    x4 = ['4    ',num2str(array(5))];
    x5 = ['5    ',num2str(array(6))];
    x6 = ['6    ',num2str(array(7))];
    x7 = ['7    ',num2str(array(8))];
    x8 = ['8    ',num2str(array(9))];
    x9 = ['9    ',num2str(array(10))];
    title = "*****SERVER TABLE*****";
    disp(title);
    disp(x0);
    disp(x1);
    disp(x2);
    disp(x3);
    disp(x4);
    disp(x5);
    disp(x6);
    disp(x7);
    disp(x8);
    disp(x9);

end