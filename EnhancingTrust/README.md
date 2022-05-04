# Getting Started

This project was bootstrapped with [Create React App](https://github.com/facebook/create-react-app). In order to run this project, first install all dependencies by running the command:
```
npm install
```

Then, just run the start command to run the project locally:
```
npm start
```

## Templates
In this project we describe templates as the HTML content for sms, emails, letters, webpages, audios and any other asset utilized for the users to test if it is real or fake.

### Adding Templates
To add a new template, you must create an HTML file in `/public` folder and in the corresponding folder type (emails, sms...). The HTML can be in any structure you want.

You must know that `link` tags will be omitted when injected in the page for the reason that adding a style this way will affect the rest of the page. If you want to add styles, then use a `style` tag. The render engine will prepend a CSS class to avoid collisions between the styles of the rest of the page.

Each template type will have a specific configuration for some static content like the email subject, sender and others. This configuration will go in the HTML file in a `script` tag with attribute `data-config`. Any other script tag will be ignored. The configuration should go as follows:
```
<script data-config>
  const Init = function () {
    return {
      subject: 'Email Subject',
      fromEmail: 'senderemail@email.com',
      fromName: 'Rudiney',
      to: 'senderemail@email.com',
      mailedBy: 'mail3.ssa.gov',
    };
  }
  Init();
</script>
```
##### Email Configuration
```
<script data-config>
  const Init = function () {
    return {
      subject: 'Email Subject',
      fromEmail: 'senderemail@email.com',
      fromName: 'Rudiney',
      to: 'senderemail@email.com',
      mailedBy: 'mail3.ssa.gov',
    };
  }
  Init();
</script>
```

##### SMS Configuration
```
<script data-config>
  const Init = function() {
    return {
      senderName: 'John Doe',
      senderNumber: '+1 (855) 558-7771'
    };
  }
  Init();
</script>
```

##### Webpages Configuration
```
<script data-config>
  const Init = function() {
    return {
      tabIcon: '/webpages/fedGovFiles/favicon.ico',
      tabName: 'Federal Goverment of the US',
      url: 'https://www.usa-federal.gov/',
      urlTooltip: 'Not the original url',
    };
  }
  Init();
</script>
```

***Note:*** Do not add html or body tags in a webpage template cause they won't be parsed correctly.

#### Letter Configuration
```
<script data-config>
  const Init = function () {
    return {
      companyInfo: {
        logo: 'https://ui-avatars.com/api/?name=Company&size=45&background=03269E&color=fff',
        name: 'H-TECH',
        slogan: 'Slogan',
        streetAddress: 'Street Address',
        addressLine: 'City State ZIP Code',
        country: 'United States',
      },
      recipientInfo: {
        name: 'John Doe',
        title: 'Software Engineer',
        streetAddress: 'Street Address',
        addressLine: 'City State ZIP Code',
      },
      salutation: 'Dear John Doe,',
      contactInfo: {
        phone: '+1 (855) 558-7771',
        email: 'john.doe@mail.com'
      },
      senderInfo: {
        name: 'Katherine Kane',
        title: 'CEO at H-TECH'
      },
      footer: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Magna etiam tempor orci eu.',
    };
  }
  Init();
</script>
```



## Workflows
We call workflows to the set (steps) of templates that needs to be evaluated by the user. Workflows are configured in `/src/config/steps.json`. In this file you define the mode (educational/test) and the steps to follow when clicking the next button.

```
{
  "workflows": [
    {
      "id": "1",
      "mode": "educational",
      "steps": [
        {
          "type": "sms",
          "template": "design.html"
        },
        {
          "type": "letter",
          "template": "design.html"
        },
        {
          "type": "email",
          "template": "design.html"
        },
        {
          "type": "audio",
          "template": "autumn.mp3"
        }
      ]
    }
  ]
}
```

Make sure every workflow has a unique ID. This ID is used and passed in the URL to know what workflow to run. For example, the URL to run the workflow above would be `/workflow/1`.
