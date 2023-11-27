---
layout: post
title: "Review eCPPTv2. "
subtitle: "Certificacion eCPPTv2 "
category: Blog
tags: [Certification, eCPPTv2]
image:
  path: /assets/img/ecppttrack/eCPPT.png
---

---

<!--more-->

1. this ordered seed list will be replaced by the toc
   {:toc}

---

# Review eCPPTv2

With much joy, I'm here to tell you, without spoilers, how to become certified as a **Certified Professional Penetration Tester** from [ElearnSecurity]. I've just obtained this certification and I want you to also get certified. I'll share my experience, tips, and tricks with you so you can achieve it on your first attempt.

[ElearnSecurity]: https://security.ine.com/certifications/ecppt-certification/

---

## Why Certify with eCPPTv2?

In August, I achieved my eJPTv2 certification. While many roadmaps suggested progressing to eWPT, I chose a different path. My ultimate goal has always been the OSCP, and certifying with eCPPTv2 has become a valuable step in my journey. I gained confidence, simultaneously shortening the distance to my primary objective.

Although the conventional route suggests eWPT, I felt that strengthening my full pivoting skills with eCPPTv2 would be beneficial. Also, when approaching this certification, I noticed that it doesn't go too much into the web part, which leads me to believe that it will perfectly complement my current skills, of course I don't rule out certifying eWPT in the future.

In this article, I'll share my experience and how I prepared to ensure I successfully met the challenge of eCPPTv2. I firmly believe that this certification, focused on full pivoting, is not only crucial for the OSCP but also for Real-World scenarios where pivoting is a commonly used skill.

---

## Recommendations before the Exam

As the saying goes, practice makes perfect. For instance, as a CTF player, I was already comfortable with pivoting using tools like Chisel and Socat, but my experience was limited to double pivoting. While this is more than sufficient for passing eCPPTv2, I firmly believe that taking your time to learn will make you a more proficient professional in the end.
For this certification, you can pivot in any way you choose—there are no limits. It's a black-box type, so you can utilize various tools, including but not limited to:

- [Chisel].
  [Chisel]: https://deephacking.tech/pivoting-con-chisel/
- [socat].
  [socat]: https://deephacking.tech/pivoting-con-socat/
- [Netsh].
  [Netsh]: https://deephacking.tech/pivoting-con-netsh/
- [ligolo-ng].
  [ligolo-ng]: https://github.com/nicocha30/ligolo-ng
- Metasploit-with-socat
- [Metasploit-with-prtfw].
  [Metasploit-with-prtfw]: https://pentest.blog/explore-hidden-networks-with-double-pivoting/
- [ssh].
  [ssh]: https://deephacking.tech/pivoting-con-ssh/
- [shuttle].
  [shuttle]: https://deephacking.tech/pivoting-con-shuttle/
- [Proxychains].
  [Proxychains]: https://deephacking.tech/pivoting-con-proxychains/
- [Plink.exe].
  [Plink.exe]: https://deephacking.tech/pivoting-con-plink-exe/

Before diving in, it's crucial to have a good understanding of what pivoting involves. I recommend the **Wreath** room on TryHackMe, but keep in mind that you need a streak of **7 days** to access this room. Answer a question or two each day, and on the seventh day, you'll be able to download the VPN and explore. This room provides excellent explanations of how each tool works, enhancing your understanding of pivoting techniques.

[wreath]: https://tryhackme.com/room/wreath

---

### Pure Metasploit

Let's cut to the chase! By now, you should already have the skills to compromise a system. What I'm going to tell you is related to pivoting, buffer overflow, and some more tricks. There are many resources on the internet, but let's start from the beginning.

The easiest way to overcome pivoting is with Metasploit. I'll provide a useful resource from [pentest.blog] and another from [hydysys.com].

In summary, you compromise the system, and if necessary, add the network range to the route with the command `run autoroute -s xx.xx.xx.x/24`, or you can also use `route add xx.xx.xx.x/24 255.255.255.0 1`. Execute `portfwd add -l xxxx -p xxxx -r xx.xx.xx.xx`, depending on your needs. Additionally, you should use the **auxiliary/server/socks_proxy** module with options like `set srvhost xx.xx.xx.xx`. Remember that this IP should be the VPN's, and you can choose between SOCKS 4a or 5 according to your preferences, which you need to edit in **/etc/proxychains4.conf** on the last line, `socks5 127.0.0.0 1080`. Repeat these steps for each host, executing the one in **/etc/proxychains4.conf** when using Metasploit; you only need to put the line `socks5 127.0.0.1 1080` once, and you're good to go! As you can see, it's quite straightforward, but let me tell you there's an even easier way if, like me, the **portfwd add** command confuses you.

[pentest.blog]: https://pentest.blog/explore-hidden-networks-with-double-pivoting/
[hydysys.com]: https://www.hdysec.com/double-pivoting-both-metasploit-and-manual/

---

### Mestasploit and Socat

It's practically the same, everything is the same, just that instead of using portfwd add, we use `socat`. This means that we redirect each connection or reverse shell through socat, and that's it, no portfwd. Everything else remains the same: the 'run autoroute' and the SOCKS proxy module.

---

### Chisel and socat

Personally, this is the method I've used the most because it's the one I master the best. However, in the end, I did all three (**Metasploit with Socat, Logolo-ng, Chisel with Socat**), and I'll explain why later. But before delving into these advanced techniques, let me share my experience with you. I've set up numerous labs because, as I mentioned before, I was already familiar with the double pivot. The labs I've created are well-known, including the two to four-node pivot from **S4vitar** and some other content creators whose links I share and recommend you explore and set up their labs. Ironically, I've noticed that there are fewer resources in English on this topic.

#### S4vitar

- [Preparación-eCPPTv2].
  [Preparación-eCPPTv2]: https://www.youtube.com/watch?v=_7b_GQDfA5M&pp=ygUPZWNwcHR2MiBzNHZpdGFy
- [PIVOTING-DESDE-CERO-#1].
  [PIVOTING-DESDE-CERO-#1]: https://www.youtube.com/watch?v=L1jSoCcvRY4&pp=ygUPZWNwcHR2MiBzNHZpdGFy -[PIVOTING-DESDE-CERO-#2].
  [PIVOTING-DESDE-CERO-#2]: https://www.youtube.com/watch?v=E4eUdAd6tAM&t=5056s&pp=ygUPZWNwcHR2MiBzNHZpdGFy
- [PIVOTING-DESDE-CERO-#3].
  [PIVOTING-DESDE-CERO-#3]: https://www.youtube.com/watch?v=sjUgh__Utvs&t=2483s&pp=ygUPZWNwcHR2MiBzNHZpdGFy -[PIVOTING-DESDE-CERO-#4].
  [PIVOTING-DESDE-CERO-#4]: https://www.youtube.com/watch?v=Mc4FuBRyybc&t=3768s&pp=ygUPZWNwcHR2MiBzNHZpdGFy -[Simulación-de-examen-eCPPTv2].
  [Simulación-de-examen-eCPPTv2]: https://www.youtube.com/watch?v=Q7UeWILja-g&t=20906s&pp=ygUPZWNwcHR2MiBzNHZpdGFy

And there are many more resources on the internet, and you might wonder, how does this help me? Well, as I mentioned earlier, practice makes perfect, so you will do it at three levels. Study well how these tools, [Chisel] and [Socat], function. Replicating the lab will be easier if you understand something about the tool.s

{:.note title="Attention"}
In the exam, it's essential to note that the versions that don't fail are the 2.5. Keep this in mind.

[chisel]: (https://github.com/jpillora/chisel)
[socat]: (https://github.com/3ndG4me/socat/blob/master/README)

#### First phase: Script Kiddie

Replicate the lab simultaneously with the tutorial. Build it exactly the same way, so you go along with them, handling errors together to avoid frustration if something goes wrong. Remember that the first way we learn as children is by observing, but in this case, we'll also be actively doing it in parallel.

#### Second phase: Training Wheels

Now that you're confident and familiar with how the lab works, don't get too comfortable. We understand and master the lab, but let's change things up. For example, if we were following in the first phase [Simulación-de-examen-eCPPTv2], aragog => naguini => fawkes => blue => matrix => brainpan, now what we'll do is change the order, like matrix => fawkes => aragog => blue => naguini => brainpan. This ensures that we're no longer dependent and can navigate through it on our own, akin to riding a bike with training wheels.

#### Third phase: Hatchlings

At this point, we should be capable of solving any set of labs independently. however, we need to challenge ourselves. just like fledglings when they prepare to leave the nest and must jump into the void, we must do the same. in this phase, let's explore platforms like [HackMyVW], [VulnHub],etc , according to your preference. download a couple of machines; i recommend only two because the goal is not to practice with every Linux machine but also with Windows. here are the links for [blue], [Academy], [Active-Directory] and mandatory, brainpan. arrange them as you like and switch their positions to keep things dynamic.

[Blue]: https://drive.google.com/file/d/1vMszZFJpmULp_l60NU7WaUla0JIw7qi9/view?usp=drive_link
[Academy]: https://drive.google.com/file/d/1u4628J7AwEzFCS3gWZbJgv-lhGzwmrvf/view?usp=drive_link
[Active-Directory]: https://mega.nz/folder/djNgEQaK#SMkGghJ6uA4dStqIypCOQw/file/pvUiFLjI
[Simulación-de-examen-eCPPTv2]: https://www.youtube.com/watch?v=Q7UeWILja-g&t=20906s&pp=ygUPZWNwcHR2MiBzNHZpdGFy
[HackMyVW]: https://hackmyvm.eu/machines/
[VulnHub]: https://www.vulnhub.com

Believe me, I assure you that if you practice a lot, you will master pivoting with Chisel and Socat. You will discover some interesting things that I noticed through so much practice, and I will tell you more about them later.

#### Others

- [eCPPTv2-Todo-lo-que-necesitas-saber]
  [eCPPTv2-Todo-lo-que-necesitas-saber]: (https://www.youtube.com/watch?v=yuQn96veqZc&t=1913s)
- [Primer-Laboratorio-Tipo-eCPPTv2]
  [Primer-Laboratorio-Tipo-eCPPTv2]: (https://www.youtube.com/watch?v=SjwyIY2OdmU&t=6950s)
- [Segundo-Laboratorio-Tipo-eCPPTv2]
  [Segundo-Laboratorio-Tipo-eCPPTv2]: (https://www.youtube.com/watch?v=9G0He3Bt4g4&t=8s)
- [Tercer-Laboratorio-Tipo-eCPPTv2]
  [Tercer-Laboratorio-Tipo-eCPPTv2]: (https://www.youtube.com/watch?v=0KN1GzeVVmI&t=1301s)
- [Laboratorio-Pivoting-eCPPT]
  [Laboratorio-Pivoting-eCPPT]: (chrome-extension://bigefpfhnfcobdlfbedofhhaibnlghod/mega/secure.html#folder/djNgEQaK#SMkGghJ6uA4dStqIypCOQw)

These are other content creators who have developed their own simulations that you can also implement. Some of them are available on the internet.

---

### Pivothing with Ligolo-ng

It's easy, you just have to follow the GitHub repository guide. Simply download the proxy and the agent on your attacking machine, and then upload the agent to the target host. Unlike previous cases with Logolo-ng, creating a VPN won't require proxychains. There are some resources on the internet that you can consult about this, but I believe that the repositories are sufficient. Nevertheless, I'll leave the links in case you want to check them out [Network-Pivoting-with-Ligolo-NG], [Xerosec] y [Ligolo-ng:-Pivoting-Your-Way], etc.

[Ligolo-ng:-Pivoting-Your-Way]: https://www.youtube.com/watch?v=msSpAYT9za8&t=3s
[Xerosec]: https://www.youtube.com/watch?v=Kimrp9WZPTU&t=987s
[Network-Pivoting-with-Ligolo-NG]: https://www.youtube.com/watch?v=DM1B8S80EvQ&t=2s

### Others Tools

Proxychains: Ideal to combine with Metasploit or Chisel.

Netsh: Performs similar functions to Socat but for Windows.

SSH : Requires the host to have SSH available, does not achieve double pivoting.

Shuttle: Requires SSH and Python3, does not achieve double pivoting.

Plink.exe: Similar to SSH for Windows, but it is quite limited.

It is valuable to explore all of these tools, as you can take advantage of them in a variety of situations, such as opening specific ports, exposing web ports and other applications.

---

## Buffer Overflow

I recommend completing all the binaries in the [Buffer-Overflow-Prep] room and finishing the [Stack-Based-Buffer-Overflows-on-Windows-x86] module. With all this, you can easily overcome the buffer overflow; it's just a matter of practice. To further raise your skill level, challenge yourself by using both Immunity Debugger and x2debug. In this way, you will also become familiar with other tools. Here are also links to [HackTheBox|Buff] and [¿Cómo-explotar-el-Buffer-Overflow-del-OSCP-con-éxito?]

[Stack-Based-Buffer-Overflows-on-Windows-x86]: (https://academy.hackthebox.com/course/preview/stack-based-buffer-overflows-on-windows-x86)
[Buffer-Overflow-Prep]: (https://tryhackme.com/room/bufferoverflowprep)
[¿Cómo-explotar-el-Buffer-Overflow-del-OSCP-con-éxito?]: (https://www.youtube.com/watch?v=sdZ8aE7yxMk&t=2296s)
[HackTheBox|Buff]: (https://www.youtube.com/watch?v=TytUFooC3kU&t=9392s)

---

## Exam

Approach the exam with confidence, but not overconfidence. You have a total of 14 days, 7 days to conquer the lab portion, and another 7 days to compose the report, which is more than sufficient, trust me, to successfully pass the exam.

At this point, I recommend thorough enumeration. If you've faced the EJPT before, you'll already be familiar with the dynamics. First and foremost, be aware that the VPN may have compatibility issues. The exam lab is somewhat outdated, so if you encounter connection problems, edit the VPN where it says cipher AES-256-CBC and modify it to --data-ciphers AES-256-CBC. That's all; now, dive in.

As always, do not despair. Trust your notes and what you have studied. You may wonder about my progress, about what I did each day. I should mention that I chose to take the exam on a 'Feriado' which is a holiday in a row, freeing me from work and life worries. I wanted to concentrate fully on the exam. In short, I started on Thursday at 8 am. It is worth noting that as I progressed through the exam, I was simultaneously taking notes and taking screenshots, creating a structured report in LaTeX. Although I don't recommend it to everyone, despite having a ready-made template from previous labs, formatting it on the fly took me a considerable amount of time.

### Day One

In about five hours, I had root access to the first host. Pay close attention to the dictionaries you use. Use the right one for each situation, not just for root, but for enumeration in general. Based on previous reviews that mentioned hints for finding the next hosts, I meticulously enumerated each system. I took post-exploitation seriously, very seriously. However, looking back, it was not as intense as I thought. The clues were obvious, and what I initially considered honeypots to throw me off turned out to be a waste of time. Nevertheless, with that, I moved on to the next one.

By about ten o'clock at night, I had the next two hosts. These were simple, the most well-known vulnerability we are all familiar with. Exploitation was immediate; as I mentioned, it was the enumeration for post-exploitation that took time. Overall, as I said, it was not as challenging as I initially thought, but as usual, I tried to enumerate everything to practice what I learned. The surprising part is that I expected to run into more difficult stuff, as I saw reviews that used Ebowla to bypass Windows Defender, but let me tell you, I didn't need any of that. It is true that some hosts have firewall rules, but once you get NT AUTHORITY SYSTEM, you disable them and that's it. After that, I went to sleep like a baby.

### Day Two

At this point, I had three hosts out of five, so it was time for the buffer overflow. This was fairly straightforward for me, since I had already dealt with all the binaries in the TryHackMe room, as well as Hack The Box machines and CTFs. It seemed like a walk in the park, especially since I already had the scripts ready; I just had to change the IP and port. In the report, I included all the scripts used and captured everything; pay attention to that detail. By noon, I had the fourth host listed thoroughly, which, as I said, may have been a bit excessive, as everything was pretty obvious. But hey, what is well learned is hard to forget. At this point, I started taking longer breaks, experiencing no setbacks or unforeseen events, except for those inherent to the exam itself, such as VPN disconnections due to fast fuzzing, which I will share with you later.

### Day Three

Moving from the fourth to the last host, I initially thought of using Metasploit, but if you're somewhat familiar with PowerShell, that's all you need. Doing it with Metasploit is easier than the multiplication table. I got the final machine up and running, and in about two or three hours, I was pwned. As I mentioned before, I had been documenting the process at the same time, but somewhere along the way, I forgot to capture screenshots and parts of the draft report. The excitement of getting it done, I guess. By the end of the third day, I had gotten it all done, but the report was missing some written sections and screenshots. However, with time to spare, I decided to call it a night and get some sleep.

### Fourth day

as I was missing captures and parts of infome, I think I lost the connection, you know the lab is unstable, but I already knew how to do it, this time, I decided to go over it with Ligolo-ng, documenting and capturing what I had missed before, making it more of a fill in the blanks exercise.

### Day five

Essentially the same as day four, but this time using Metasploit and Socat. It took me about two hours, almost as if it were done with just pure Metasploit. I did this to reinforce what I had learned, practicing it immediately if I missed or forgot something.

### Day six

I devoted the whole day to completing the report. I already had about 70% of it, but formatting in LaTeX is a headache. Creating tables, command boxes, images and those final details, as I am meticulous with those things. So I spent the whole day on it, and in the evening I submitted it. That was all said and done. Several days later, the certificate was available. In short, it seemed normal to me because, truth be told, I prepared and studied. However, I remember seeing reviews before and it seemed easier than it looks. And it is true.

---

## Exam Recommendations

- Have a template ready for the report. I used [CheckN8] as a guide. Don't make life harder for yourself; use Word or LibreOffice, unlike me, who used LaTeX.

[CheckN8]: https://assets.tryhackme.com/additional/wreath-network/writeups/CheckN8%20-%20Wreath.pdf

- Keep your notes handy. With numerous commands and tools, it's impossible to memorize everything.

![list](/assets/img/ecppttrack/1.png){:.lead width="800" height="100" loading="lazy"}

- Work on the report concurrently, but don't forget to write and capture. You might not have enough time for a second pass.

- When fuzzing with tools like Nmap, SQLMap, or any web fuzzer, do it cautiously. I experienced lab disconnections when fuzzing too quickly.

- If the lab disconnects, before restarting, ensure you genuinely have no connection. Sometimes, only the VPN drops.

- You can only restart the lab four times per day. Be cautious.

- Investigate the difference between the following as it will be very common in situations where you think you are not doing something right and you are not reusing the port you have opened, this is useful for bringing things up or reverse-shell.

```bash
./socat TCP-LISTEN:2222,fork TCP:192.168.1.7:1111
# and .
./socat tcp-l:2222,fork,reuseaddr tcp:192.168.1.7:1111
```

- Stay organized, especially with multiple open windows for servers with Chisel or clients. It's easy to get lost.

![list](/assets/img/ecppttrack/19.png){:.lead width="800" height="100" loading="lazy"}

- I used Kitty to manage windows efficiently. In one window, I placed all the lights, which are connections with the server. If everything is correct, the server's Chisel connection appears; otherwise, something is wrong.

![list](/assets/img/ecppttrack/32.png){:.lead width="800" height="100" loading="lazy"}

- Concerning bridges (socat / netsh), previously, I opened a port and left the process there. This is extremely inefficient, as you're wasting host resources on socat, which could crash the VPN. What I did is put the bridges on the back burner.

```bash
#For Linux:
./socat tcp-l:2222,fork,reuseaddr tcp:192.168.1.7:1111 &
#For Windows:
start chisel.exe client 10.10.0.131:3333 R:1082:socks
```

![list](/assets/img/ecppttrack/9.png){:.lead width="800" height="100" loading="lazy"}

- If you forget which port you used, use ProxyChains with Nmap to see open ports:

```bash
proxychains nmap --top-ports 100 --open -T3 -v -n 10.10.10.128 -sT -Pn 2>&1 | grep -vE "timeout|OK|denied"
```

Similarly, check for open ports:

```bash
proxychains nmap --open -v -n -sCV -p21,22,80,139,445 10.10.10.128 -sT -Pn -oN target 2>&1 | grep -vE "timeout|OK"
```

- Learn to use nc or others for port enumeration.

- It's essential to master resource escalation through pivoting. If you're in Matrix and want to bring up Chisel but don't have SSH, you should be able to bring that resource through all the tunnels you've created. Believe me, this is fundamental, and if you know this, you've mastered pivoting.

- Study the difference between strict chain and dynamic chain. Depending on what you're using, you may or may not pass through ProxyChains. The same goes for the web part. It's curious that you just put a proxy, and it opens from all IPs. This is phenomenal, the same for running scripts.

![list](/assets/img/ecppttrack/33.png){:.lead width="800" height="100" loading="lazy"}

![list](/assets/img/ecppttrack/83.png){:.lead width="800" height="100" loading="lazy"}

- I'm not sure if others do this, but I cleaned up, meaning I left the system as I found it. I didn't create persistence or enable SSH. So, for the cleanup part, I only had to remove Chisel and Socat, history, and logs. Chisel and Socat leave quite a bit of logs when enumerating. I'm not sure if they're stder or stdout, but I tried to leave the system as I found it. For example, if I brought down the firewall, I raised it again and did the same with everything else.

- Regarding determining the vector of a vulnerability, I used [first.org] to calculate the vulnerability's vector. This is only for those you interact with on the host, not for others. You probably know more about this.

[first.org]: https://www.first.org/cvss/calculator/3.1

- Use CherryTree to store the outputs of each command. I initially thought this would be useful because someone could replicate the exam with your report and grade you. Now, I'm not so sure.

- To avoid overloading the server and prevent putting too much stress on it, I streamlined my enumeration using only one-liners. Examples:

![list](/assets/img/ecppttrack/18.png){:.lead width="800" height="100" loading="lazy"}

![list](/assets/img/ecppttrack/25.png){:.lead width="800" height="100" loading="lazy"}

![list](/assets/img/ecppttrack/69.png){:.lead width="800" height="100" loading="lazy"}

## Conclution

"I'm not telling you to follow everything I say to the letter. What I'm trying to convey is that if you study conscientiously, you can earn this certification and any other. I won't say it's easy because in life, nothing is easy. In summary, study, take notes on everything, capture everything, and if you get stuck, rest, breathe, backtrack, review your notes, think outside the box. You might face this more than once, so come back. Without much else to tell you, just want to say, see you in OSCP."
