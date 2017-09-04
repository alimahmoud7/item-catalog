from app.models import *

# Make a connection between class definitions and the corresponding tables within database

# Establish a link of connection between code execution and the engine

# User 1
user = User(name='Ali Mahmoud', email='ali.mahmoud@engineer.com', picture='/static/img/user-ali.png')
user2 = User(name='User Name', email='username@gmail.com', picture='/static/img/user2.jpg')
user3 = User(name='John Doe', email='john.doe@gmail.com', picture='/static/img/default-user.png')

# Field 1
field1 = Field(name='Web Development', user=user)
session.add(field1)
session.commit()

mooc1 = MOOC(title='Front End Frameworks', provider='Udacity', creator='Google', level='Advanced',
             url='https://www.udacity.com/course/front-end-frameworks--ud894',
             description="Explore and build interactive, single-page applications with popular JavaScript frameworks",
             image='https://lh3.googleusercontent.com/8pON7YYmLDJk7IymiYvvylNLGvLC2-fAGwcSKKli_tdwskej0z-ZIV8iM50hzh3yBJcEhjEkc7-CK6b4nMI=s0#w=1920&h=1080=s276#w=1724&h=1060',
             field=field1, user=user)
session.add(mooc1)
session.commit()

mooc2 = MOOC(title='Full Stack Foundations', provider='Udacity', creator='Amazon Web Services', level='Intermediate',
             url='https://www.udacity.com/course/full-stack-foundations--ud088',
             description="Learn the fundamentals of back-end web development by creating your own web application from the ground up using the iterative development process.",
             image='https://lh3.ggpht.com/GKNi4exuLn_ER_qN9SIPx4bFpjBhVBGeSP1aTul1hh_Ge_9oRREpLimJyphdkJqc8sgwRo-GQ0vgSO3KcnY=s0#w=1745&h=1073',
             field=field1, user=user2)
session.add(mooc2)
session.commit()

mooc3 = MOOC(title='Intro to JavaScript', provider='Udacity', creator='Udacity', level='Beginner',
             url='https://www.udacity.com/course/intro-to-javascript--ud803',
             description="Learn the fundamentals of JavaScript, the most popular programming language in web development.",
             image='https://lh3.googleusercontent.com/ihDVPNChYL9xwjDejhDQj-1VA1OWCRvYZFdMh5qmDdAxCRuUjwEZMUBs5mUHQ_w9NzVy3MibrmR3m5kO8rI=s0#w=654&h=402=s276#w=1724&h=1060',
             field=field1, user=user3)
session.add(mooc3)
session.commit()

# Field 2
field2 = Field(name='Cybersecurity', user=user)
session.add(field2)
session.commit()

mooc4 = MOOC(title='Cybersecurity and Its Ten Domains', provider='Coursera', creator='University System of Georgia', level='Beginner',
             url='https://www.coursera.org/learn/cyber-security-domain',
             description="This course is designed to introduce students, working professionals and the community to the exciting field of cybersecurity.",
             image='https://d3njjcbhbojbot.cloudfront.net/api/utilities/v1/imageproxy/https://coursera-course-photos.s3.amazonaws.com/e9/957fe0702411e4a0b53d9470331d4e/ComputerLock-Logo_2.png?auto=format%2Ccompress&dpr=1&w=100&h=100&fit=fill&bg=FFF',
             field=field2, user=user2)
session.add(mooc4)
session.commit()

mooc5 = MOOC(title='Web Security Fundamentals', provider='edX', creator='KULeuvenX', level='Introductory',
             url='https://www.edx.org/course/web-security-fundamentals-kuleuvenx-websecx',
             description="Essential knowledge for every web developer, discover important principles of modern web security, and learn about current security best practices.",
             image='https://www.edx.org/sites/default/files/course/image/promoted/web-security-fundamentals-kuleuvenx378225-.jpg',
             field=field2, user=user)
session.add(mooc5)
session.commit()

# Field 3
field3 = Field(name='Artificial Intelligence', user=user2)
session.add(field3)
session.commit()

mooc6 = MOOC(title='Intro to Artificial Intelligence', provider='Udacity', creator='Udacity', level='Intermediate',
             url='https://www.udacity.com/course/intro-to-artificial-intelligence--cs271',
             description="This course will introduce you to the basics of AI. Topics include machine learning, probabilistic reasoning, robotics, computer vision, and natural language processing.",
             image='https://lh3.ggpht.com/DlphLMafw8ni4x7O98V2LyrnKDxsFJpEuuC-kuLyGbYHLYmdwnpu490a8isnp6j_vh-Y_sKCX8N_NUi1wM8=s0#w=436&h=268',
             field=field3, user=user3)
session.add(mooc6)
session.commit()

mooc7 = MOOC(title='Machine Learning', provider='Coursera', creator='Stanford University', level='Intermediate',
             url='https://www.coursera.org/learn/machine-learning',
             description="This course provides a broad introduction to machine learning, datamining, and statistical pattern recognition.",
             image='https://d3njjcbhbojbot.cloudfront.net/api/utilities/v1/imageproxy/https://coursera.s3.amazonaws.com/topics/ml/large-icon.png?auto=format%2Ccompress&dpr=1&w=100&h=100&fit=fill&bg=FFF',
             field=field3, user=user2)
session.add(mooc7)
session.commit()

# Field 4
field4 = Field(name='Computer Networks', user=user3)
session.add(field4)
session.commit()

mooc8 = MOOC(title='Computer Networking', provider='Udacity', creator='Georgia Institute of Technology', level='Intermediate',
             url='https://www.udacity.com/course/computer-networking--ud436',
             description="This is an advanced Computer Networking course that delves into the latest concepts and tools used by the CN industry.",
             image='https://lh3.ggpht.com/PwqnZYeOVbWr4a3Qn3WkmZNzRlf6acf7EbQoGCBAqrmn1pOFrsX5vVr4WUHGTOaqslvjDY864Q8X2-o9ENU=s0#w=1725&h=1060',
             field=field4, user=user2)
session.add(mooc8)
session.commit()

mooc9 = MOOC(title='Computer Networks and the Internet', provider='edX', creator='kironX', level='Introductory',
             url='https://www.edx.org/course/computer-networks-internet-kironx-fhlcnx',
             description="Gain profound knowledge of how computer networks function overall, as well as how they apply to the Internet as a whole.",
             image='https://www.edx.org/sites/default/files/course/image/promoted/kommunikationsnetze_kursgrafik_1378_225.jpg',
             field=field4, user=user)
session.add(mooc9)
session.commit()

# Field 5
field5 = Field(name='Software Engineering', user=user)
session.add(field5)
session.commit()

mooc10 = MOOC(title='Software Testing', provider='Udacity', creator='Udacity', level='Intermediate',
              url='https://www.udacity.com/course/software-testing--cs258',
              description="Learn how to catch bugs and break software as you discover different testing methods that will help you build better software.",
              image='https://lh4.ggpht.com/5ikgV5XANy8ChkjUqGy4YG-4MCiREXo-SZ7p7YEFqCqIpmJ34TqTofWjG8Nz6RlxzNmgtDQxAeLeLsbE-8Kh=s0#w=436&h=268',
              field=field5, user=user)
session.add(mooc10)
session.commit()

mooc11 = MOOC(title='Software Engineering Essentials', provider='edX', creator='TUMx', level='Introductory',
              url='https://www.edx.org/course/software-engineering-essentials-tumx-seecx',
              description="Learn agile methods, object-oriented programing and best practices for analysis, design, testing and management in software engineering.",
              image='https://www.edx.org/sites/default/files/course/image/promoted/applied_software_378x225.jpg',
              field=field5, user=user3)
session.add(mooc11)
session.commit()

# Field 6
field6 = Field(name='Programming Languages', user=user3)
session.add(field6)
session.commit()

mooc12 = MOOC(title='Programming Foundations with Python', provider='Udacity', creator='Udacity', level='Intermediate',
              url='https://www.udacity.com/course/programming-foundations-with-python--ud036',
              description="Introductory programming class to learn Object-Oriented Programming, a must-have technique to reuse and share code easily. Learn by making projects that spread happiness!",
              image='https://s3-us-west-1.amazonaws.com/udacity-content/course/images/ud036-0619766.jpg',
              field=field6, user=user3)
session.add(mooc12)
session.commit()

mooc13 = MOOC(title='Algorithms, Part I', provider='Coursera', creator='Princeton University', level='Intermediate',
              url='https://www.coursera.org/learn/algorithms-part1',
              description="This course covers the essential information that every serious programmer needs to know about algorithms and data structures",
              image='https://d3njjcbhbojbot.cloudfront.net/api/utilities/v1/imageproxy/https://coursera.s3.amazonaws.com/topics/algs4partI/large-icon.png?auto=format%2Ccompress&dpr=1&w=100&h=100&fit=fill&bg=FFF',
              field=field6, user=user)
session.add(mooc13)
session.commit()

field7 = Field(name='Embedded systems', user=user)
session.add(field7)
session.commit()

field8 = Field(name='Game Development', user=user3)
session.add(field8)
session.commit()

field9 = Field(name='Digital Marketing', user=user)
session.add(field9)
session.commit()

# Field 10
field10 = Field(name='Android', user=user)
session.add(field10)
session.commit()

mooc14 = MOOC(title='Android Development for Beginners', provider='Udacity', creator='Google', level='Beginner',
              url='https://www.udacity.com/course/android-development-for-beginners--ud837',
              description="Learn the basics of Android and Java programming, and take the first step on your journey to becoming an Android developer!",
              image='https://s3-us-west-1.amazonaws.com/udacity-content/course/images/ud837-ca6af35.jpg',
              field=field10, user=user)
session.add(mooc14)
session.commit()

mooc15 = MOOC(title='Developing Android Apps', provider='Udacity', creator='Google', level='Intermediate',
              url='https://www.udacity.com/course/new-android-fundamentals--ud851',
              description="Build a cloud-connected Android app, and learn the tools, principles, and best practices of mobile and Android development that you'll apply to your own projects.",
              image='https://lh3.googleusercontent.com/lBvoF-3vRHVY87AX6f2g1R7VU8kkSAYw4Qp8fodFkpykiThDBq4x3zzrbbfH-CpnviftCDDp_lOWzVN8bw=s0#w=640&h=525=s276#w=1724&h=1060',
              field=field10, user=user2)
session.add(mooc15)
session.commit()

field11 = Field(name='IOS', user=user3)
session.add(field11)
session.commit()

mooc16 = MOOC(title='iOS App Development Basics', provider='Coursera', creator='University of Toronto', level='Intermediate',
              url='https://www.coursera.org/learn/ios-app-development-basics',
              description=" iOS App Development Basics, the second course in the iOS App Development with Swift specialization",
              image='https://d3njjcbhbojbot.cloudfront.net/api/utilities/v1/imageproxy/https://coursera-course-photos.s3.amazonaws.com/5f/aeb99037b611e5b05023ed9581e91a/ioslogo4.jpg?auto=format%2Ccompress&dpr=1&w=100&h=100&fit=fill&bg=FFF',
              field=field11, user=user3)
session.add(mooc16)
session.commit()

mooc17 = MOOC(title='Server-Side Swift', provider='Udacity', creator='IBM', level='Intermediate',
              url='https://www.udacity.com/course/server-side-swift--ud1031',
              description="In this course, you'll learn how to utilize Swift as a server-side language for building end-to-end applications. That's one language (Swift) for the client and server.",
              image='https://s3-us-west-1.amazonaws.com/udacity-content/course/images/ud1031-72cdb44.jpg',
              field=field11, user=user)
session.add(mooc17)
session.commit()

field12 = Field(name='Data Science', user=user2)
session.add(field12)
session.commit()

field13 = Field(name='Data Analytics', user=user)
session.add(field13)
session.commit()

print("Added CS Fields and MOOCs!")
