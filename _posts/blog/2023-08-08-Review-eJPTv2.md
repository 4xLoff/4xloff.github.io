---
layout: post
title: "Review eJPTv2. "
subtitle: "Certificacion eJPTv2 "
category: Blog
tags: [Certification,eJPTv2]
image:
  path: /assets/img/ejpttrack/cert.png
---

***

<!--more-->

1. this ordered seed list will be replaced by the toc
{:toc}

***

# Review eJPTv2

With much joy, I'm here to tell you, without spoilers, how to become certified as a **Junior Penetration Tester** from [ElearnSecurity]. I've just obtained this certification and I want you to also get certified. I'll share my experience, tips, and tricks with you so you can achieve it on your first attempt.

[ElearnSecurity]: https://elearnsecurity.com/product/ejpt-certification/


## Why Certify with eJPTv2

The first reason, in my opinion, is because you have a strong desire to learn, and besides, it's a junior certification, making it perfect for starting out. But don't get too comfortable. Putting aside the romanticism, I don't know about other parts of the world, but in Latin America, and more specifically in Ecuador, you absolutely need certifications to validate your knowledge. They always ask for **CEH** and **OSCP** at the very least. You might ask, then, why do I recommend certifying with EJPTv2? Just like in life, can't you walk before you run? If you dive into OSCP too soon, you might get overwhelmed, frustrated, and not know what to do in the high-stress situation that OSCP is. You could also end up losing **$1600**. However, if you're a prodigy and immune to the trivialities that affect us humans, you can skip ahead. But if you're more cautious like me, and you want a solid foundation, and you want to practice extensively so there's not even a millimeter of possibility to fail, then you have the **EJPTv2** certification to gain confidence and experience in the context of a multi-day exam.

## Recommendations before the Exam

- Practice a lot, a lot, a lot. If you don't know where to start, I'm actually following the OSCP path myself. I've created a [Track] of machines that could appear in the eJPTv2 exam. The best part is that you won't have to pay for VIP access because all the machines are in the free section. I've chosen this option because, perhaps, this might be our first certification and we might not be able to afford VIP subscriptions for platforms like **Hack The Box**, **TryHackMe**, etc. I've also configured the machines in such a way that each subsequent machine is related to the ones you practiced before. For example, if you've completed the first eight machines following my guide or others' content, when you reach the ninth machine, it will contain elements from what you've seen in the previous ones. While there might always be something new, I've structured it this way to avoid frustration and the constant need to consult guides just to gain admin access. By the time you complete the first machine, if not entirely, you'll feel like a real hacker, hahaha! You'll experience an indescribable sense of satisfaction.

[Track]: (https://4xloff.github.io/blog/Road-to-eJPTv2.html)

- In other reviews, I often read that EJPTv2 is not a CTF **Capture The Flag** and shouldn't be treated as one. I'm sorry to say, but this is true. It's not a CTF. You need to put yourself in the mindset of a real pentest. The difference lies in the fact that in CTFs, you're after the root flag, and that's it. Here, it's different. You have to enumerate all the servers and explore all possibilities. Of course, for this, [INE] prepares you with a course of around 150 hours, divided into 4 sections, 121 labs, etc. However, as I mentioned earlier, nothing stops you from preparing beforehand or alongside the course. On another note, the exam consists of 35 machines in 48 hours. By the way, if you're curious, it took me around 20 hours to complete. I'll explain why in the next point.

[INE]: (https://my.ine.com/CyberSecurity/learning-paths/61f88d91-79ff-4d8f-af68-873883dbbd8c/penetration-testing-student)

- As a CTF player for over three years, I initially thought I could breeze through the EJPTv2 exam. I estimated it would take about ten hours or so, and I also planned to do it manually, skipping some modules I already knew and others that didn't interest me, such as everything related to Metasploit. I prefer to perform tasks manually, and I use Metasploit only as a sort of command and control tool. However, after some careful consideration, I put aside my arrogance and embraced humility. When you think about it, you're learning and reinforcing new topics as well as revisiting concepts you might have forgotten or taken for granted. I learned a lot and didn't skip anything. I completed all the labs and even repeated some of them multiple times. For instance, I encountered six servers, all relatively straightforward, until I hit a WordPress machine. You might think, "A WordPress machine? Easy." I thought the same, but it turned out to be more complex than anticipated. It was the one that took me the longest. In my mind, I initially thought about plugins and that's it, but it turned out to be slightly more intricate. I had to script something like **xmlrpc.php**, a task more aligned with eWPT.

- There are many EJPT **cheat sheets** available online, but most of them are lackluster in terms of practicality. That's why I recommend creating your own cheat sheet. You can use tools like Obsidian, Notion, or even just a Word document. The key is that you make it yourself. Let me explain why. The act of writing will stimulate your brain more, helping you remember concepts better. There's a saying, **Practice makes perfect,** but I prefer another one that goes, **If you want to be good at something, learn slowly, because later you'll be able to do it perfectly.** However, if you still want a practical cheat sheet, I recommend the best one I found, and it's from INE as well.


![list](/assets/img/ejpttrack/cheet.png){:.lead width="800" height="100" loading="lazy"}


[cheetsheet]: (https://blog.syselement.com/ine/courses/ejpt/ejpt-cheatsheet)

## Exam Recommendations

- Approach the exam with confidence, not overconfidence. You have **48 hours**, which should be sufficient to address everything outlined in the questions. Here, I recommend thorough enumeration because, similar to the real world, if you do this well, you'll secure at least 20 exam questions, if not more. Also, here's a crucial tip: even before taking any action, go through the exam questions. Many of them provide valuable information such as users, vectors, etc. Furthermore, **read the questions carefully, and read them two or three times if necessary**.

Just like before, take notes on everything because if the server loses connectivity, you'll get disconnected, and anything within the server will be lost. I kept everything physically noted, so when I got disconnected, I had everything on hand and could continue smoothly. Rest assured, the server reboots in terms of data it contains, not shifting to a different target. That remains intact.

- As I mentioned earlier, due to my initial arrogance, I wanted to handle everything manually and under my conditions. However, this would have been a significant mistake. The server is set up with a Guacamole instance and doesn't have external internet access. Therefore, I couldn't use any exploits that weren't on the server. This posed a significant challenge. That's why it's beneficial to not skip anything related to Metasploit.

- The following point ties into the previous one. Many things require preparation before facing them. I'll tell you this, even though I haven't seen it in other reviews. I'm accustomed to SecLists and dictionaries ready for web enumeration. However, this becomes a significant problem on the server because these resources don't exist there. You have to work with what's on the server. Let me tell you, finding a dictionary that's remotely useful for this purpose is quite a challenge. You might need to try numerous options. Additionally, I can't forget to mention, while on this topic, that **brute forcing is fundamental in this certification**. You must master it thoroughly and have the precise dictionaries. Otherwise, you won't get results. I recommend you start noting down these dictionaries while you're preparing with the INE course.

- As a final point, after utilizing tricks and thorough enumeration, **I suggest responding to the exam questions based on their content**. This approach is more efficient and better. It's possible that you won't need to exploit something in certain cases, and this can save time for more critical moments. With all this in mind, you should have some time left over. I recommend reviewing the questions and verifying your answers meticulously. In my opinion, there might be tricky questions. Without further ado, I'll see you in the **eCPPTv2**.
