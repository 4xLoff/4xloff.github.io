---
layout: post
title: "Review OSWP. "
subtitle: "Certificacion OSWP "
category: Blog
tags: [Certification, OSWP]
image:
  path: /assets/img/oswp/oswp.png
---

---

<!--more-->

1. this ordered seed list will be replaced by the toc
   {:toc}

---

# Review OSWP

It is with great joy that I am here to tell you, without spoilers, how to get certified as an [OSWP] **Offensive Security Wireless Professional**. I just got this certification and I want you to get certified too. I'll share with you my experience, tips and tricks so you can get it on your first try.

[Offsec]https://www.offsec.com/courses/pen-210/

---

## Why Certify with OSWP?

In this article I will share my experience and how I prepared myself to successfully meet the challenge of OSWP, actually I am preparing for OSCP, but I bought the learner one that gives you the possibility to take this exam, I have taken advantage and I have been certified, all the resources that I will tell you have helped me a lot to achieve the goal, but I'm not going to fool you I already start with an advantage because I started the hacking world when I was a child booteaba on a usb distribution for wireless pentesting, ie doing the pranks we usually do when we are small and comprotetia personal networks WPS, WEP, WPA-PSK, WPA2-PSK, etc· and the MGT very few as we are so common, also served to reecordar, in short let's move to the important thing·

---

## Recommendations before the Exam

As the saying goes, practice makes perfect, in the resources that you get in offsec the laboratirios you must assemble them yourself and that is tedious because you must have a moden, a wireless card, etc·

To avoid this we will use some fancy resources created by [_r4ulcl_] called WiFiChallengeLab, which we will use them to practice the challenges of the challenger itself, but we will use them to make all the challenges of OSWP since the APs and clients are mounted in virtualvox inside the docker or image, these will not simplify much·

[_r4ulcl]@_r4ulcl_

- [WiFiChallengeLab](https://github.com/r4ulcl/WiFiChallengeLab)
- [WiFiChallengeLabv2.0](https://github.com/r4ulcl/WiFiChallengeLab)

Well, but in addition to that we will practice a lot with the resources of [attackdefense·pentesteracademy·com](https://attackdefense·pentesteracademy·com):

### Basic

- [WiFi Traffic Analysis](https://attackdefense.pentesteracademy.com/listing?labtype=wifi-security-basics&subtype=wifi-security-basics-traffic-analysis)
- [Reconnaissance](https://attackdefense.pentesteracademy.com/listing?labtype=wifi-security-basics&subtype=wifi-security-basics-recon)
- [AP Client Basics](https://attackdefense.pentesteracademy.com/listing?labtype=wifi-security-basics&subtype=wifi-security-basics-ap-client-basics)
- [Tools](https://attackdefense.pentesteracademy.com/listing?labtype=wifi-security-basics&subtype=wifi-security-basics-tools)

### Personal Networks

- [Offline Cracking](https://attackdefense.pentesteracademy.com/listing?labtype=wifi-security-personal-networks&subtype=wifi-security-personal-networks-offline)
- [Live Cracking](https://attackdefense.pentesteracademy.com/listing?labtype=wifi-security-personal-networks&subtype=wifi-security-personal-networks-live)

### Enterprise Networks

- [Offline Cracking](https://attackdefense.pentesteracademy.com/listing?labtype=wifi-security-enterprise-networks&subtype=wifi-security-enterprise-networks-offline)
- [Live Cracking](https://attackdefense.pentesteracademy.com/listing?labtype=wifi-security-enterprise-networks&subtype=wifi-security-enterprise-networks-online)
- [Pivoting](https://attackdefense.pentesteracademy.com/listing?labtype=wifi-security-enterprise-networks&subtype=wifi-security-enterprise-networks-pivoting)


### Other Resources

- [Wi-Fi-Pentesting-Cheatsheet](https://github.com/dh0ck/Wi-Fi-Pentesting-Cheatsheet)
- [WirelessPentesting-CheatSheet](https://github.com/V0lk3n/WirelessPentesting-CheatSheet)
- [oswp-preparacion/#](https://s4vitar.github.io/oswp-preparacion/#)

---

## Exam

The first thing will be to verify all the requirements such as having your identification on hand, following the steps· The truth is they are very simple· This will take about 15-20 minutes· If everything is correct, the exam lasts 3 hours and 45 minutes· You must commit two of three networks, one of which is mandatory, so you have to commit to it, no matter what·

## Conclution

Personally, I believe that this certification is quite neglected in terms of resources and labs, it's much inferior to the OSCP, but overall I liked it. Even though there's a lot of theory, if you combine it properly and can deploy and execute everything, the practical exercises will go very well. Allow me to share some tips for real-life audits: if you create your AP with login pages, you'll have a better chance of obtaining credentials. For handshakes, launch the karma attack first, even if it's very noisy; no one says anything. I don't know why they don't implement more solutions. Regarding security against brute force attacks, the dictionary is the most important. The more specific data you have, the more chances you'll have of obtaining credentials. But, as I said, the mischievous AP is better. I hope I've helped you!
