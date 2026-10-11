# Repose Spa & Wellness

<p align="center">
  <img
    src="documentation/images/features/responsive-repose.png"
    alt="Responsive preview of the Repose Spa & Wellness website across multiple screen sizes"
    width="700"
  >
</p>

Repose Spa & Wellness is a full-stack Django booking and membership platform created for a fictional London spa and wellness business.

Visitors can explore treatments, spa packages and membership benefits, while the booking flow allows customers to reserve spa access, treatments or packages and complete payment securely through Stripe Checkout. Registered users can view their confirmed bookings and membership information through their personal account area, while active members receive additional benefits such as complimentary spa access and discounted standalone treatments.

The project was designed around a calm, minimal user experience that reflects the Repose brand while keeping the booking and payment process clear and easy to follow across mobile, tablet and desktop devices.

## Live Site

- [View the live Repose Spa & Wellness website](https://repose-cff44b1bb103.herokuapp.com/)

---

## Table of Contents

- [User Experience](#user-experience)
- [Wireframes](#wireframes)
- [Application Features](#application-features)
- [Booking & Membership Development](#booking--membership-development)
- [Design & Accessibility](#design--accessibility)
- [User Stories](#user-stories)
- [Future Features & Improvements](#future-features--improvements)
- [Entity Relationship Diagram](#entity-relationship-diagram)
- [Data Model](#data-model)
- [Technologies Used](#technologies-used)
- [Testing](#testing)
- [Bugs](#bugs)
- [Deployment](#deployment)
- [Credits](#credits)

---

# User Experience

## Strategy

### Purpose

The purpose of Repose Spa & Wellness is to provide a clear and accessible platform where customers can explore spa services, make bookings and purchase annual memberships online.

The application combines booking functionality, secure payments and personal account features while allowing the business to manage treatments, packages, bookings and memberships through Django Admin.

### User Needs

Users should be able to:

- Quickly understand what Repose Spa & Wellness offers.
- Explore the Home, About, Treatments, Packages and Membership pages without creating an account.
- Compare treatments and packages using clear descriptions, prices and durations.
- Understand membership benefits and pricing before purchasing.
- Book spa access, treatments or packages through a simple, structured booking flow.
- Select valid booking dates, times and guest quantities.
- Review booking details and the total price before payment.
- Complete payments securely through Stripe Checkout.
- Register and log in to access personalised account features.
- View upcoming and previous confirmed bookings through My Account.
- Purchase an annual membership and view its status and validity dates.
- Receive eligible membership discounts on standalone treatments.
- Log out securely.
- Use the website comfortably across mobile, tablet and desktop devices.

### Site Owner Goals

The site owner should be able to:

- Present treatments and spa packages clearly to potential customers.
- Accept online bookings for spa access, treatments and packages.
- Sell annual memberships through the website.
- Perform CRUD operations on treatments, packages and other relevant records through Django Admin.
- Update service information through the database rather than editing page templates.
- Keep booking and payment records organised.
- Reliably distinguish between pending, completed and cancelled payment attempts.
- Apply membership-specific benefits and booking rules consistently.


## UX Design Approach

Repose Spa & Wellness uses a minimal and uncluttered interface. The visual design is intended to reflect the calm and relaxing experience associated with the Repose brand rather than overwhelm users with unnecessary visual elements.

The layout focuses on clear navigation, generous spacing, restrained colours and clearly defined calls to action. The purpose of this is to make it easy for visitors to locate treatments, packages, membership information and the booking process without unnecessary distractions.

The booking journey follows the same principle by dividing the process into individual steps rather than presenting one large form. Users first choose what they would like to book, then select booking details, enter guest information, review the booking and finally continue to Stripe Checkout.

---

## Wireframes

- The wireframes were created to establish the basic layout and structure of Repose Spa & Wellness before development.
    Separate mobile, tablet and desktop layouts illustrate how the interface adapts to different screen sizes.

<table>
  <tr>
    <th>Mobile</th>
    <th>Tablet</th>
    <th>Desktop</th>
  </tr>
  <tr>
    <td><img src="documentation/images/responsive/wireframe-mobile.png" alt="Initial Repose mobile wireframe" width="200" height="auto"></td>
    <td><img src="documentation/images/responsive/wireframe-tablet.png" alt="Initial Repose tablet wireframe" width="300" height="auto"></td>
    <td><img src="documentation/images/responsive/wireframe-desktop.png" alt="Initial Repose desktop wireframe" width="400" height="auto"></td>
  </tr>
</table>


---

# Application Features

## Core Features

Repose includes:

- Full CRUD functionality for administrative data management, allowing authorised administrators to create, read, update and delete treatments, packages, bookings, memberships and other relevant records through Django Admin.
- Public pages for About, Treatments, Packages and Membership information.
- Database-driven treatment and package content.
- User registration, login and logout.
- Responsive mobile-first navigation with an animated hamburger menu.
- Multi-step booking for spa access, treatments and packages.
- Date, time and guest selection with backend validation.
- Stripe Checkout for booking and membership payments.
- Stripe webhooks for completed and expired Checkout Sessions.
- Personal account page showing upcoming bookings, previous bookings and membership status.
- Annual membership purchase linked directly to the authenticated user.
- Automatic member treatment discount rules.
- Django Admin management for application data.
- Custom 404 page for invalid URLs.

## Site Pages

### Home Page

The Home page introduces the Repose brand through a large hero image and introductory content. Four fully clickable image cards provide access to About Us, Treatments, Packages and Membership, with subtle hover effects to improve visual feedback and navigation.

<p align="center">
  <img
    src="documentation/images/features/homepage.png"
    alt="Repose Spa & Wellness homepage"
    width="700"
  >
</p>

<p align="center">
  <img
    src="documentation/images/features/homepage-cards.png"
    alt="Repose homepage feature cards linking to the main site sections"
    width="700"
  >
</p>

On larger screens, navigation links are displayed horizontally to provide a clear and accessible layout. On smaller screens, the navigation collapses into a hamburger menu to prevent overcrowding and maintain a clean, user-friendly design.

The navigation also adapts based on the user's authentication status. Visitors who are not logged in can access the Login and Register pages, while authenticated users are presented with a My Account option instead.


<table>
  <tr>
    <th>Desktop - Logged In</th>
    <th>Desktop - Logged Out</th>
    <th>Mobile Navigation</th>
  </tr>
  <tr>
    <td>
      <img
        src="documentation/images/features/navbar-desktop-loggedin.png"
        alt="Repose desktop navigation for logged-in users"
        width="300"
      >
    </td>
    <td>
      <img
        src="documentation/images/features/navbar-desktop-loggedout.png"
        alt="Repose desktop navigation for logged-out users"
        width="300"
      >
    </td>
    <td>
      <img
        src="documentation/images/features/navbar-mobile.png"
        alt="Repose mobile navigation with hamburger menu"
        width="300"
      >
    </td>
  </tr>
</table>


### About Page

The About page introduces Repose Spa & Wellness and provides visitors with information about the spa and its facilities.

<p align="center">
  <img
    src="documentation/images/features/about-page.png"
    alt="Repose Spa & Wellness About page"
    width="700"
  >
</p>

### Treatments Page

The Treatments page displays active treatments retrieved from the database, organised into three categories: Massage, Body Treatments and Facials.

Each treatment card displays the treatment name, description, duration and price. Clicking on a treatment card takes the user to the booking page, where they can select their booking type and preferred treatment.

<p align="center">
  <img
    src="documentation/images/features/treatment-page.png"
    alt="Repose treatments page showing treatment cards"
    width="700"
  >
</p>

- Repose members receive a 15% discount on standalone treatments. The discount is automatically applied during the booking process, ensuring that members receive the correct price.

### Packages Page

The Packages page displays spa packages retrieved from the database. Each package card presents a description, included services, duration and price.

<p align="center">
  <img
    src="documentation/images/features/packages-page.png"
    alt="Repose packages page showing available spa packages"
    width="700"
  >
</p>

- Package inclusions are stored as multi-line text and displayed as a list, allowing the content to be updated through Django Admin without modifying the template.

### Membership Page

The Membership page explains the annual Repose membership and its benefits.

Membership benefits include:

- Complimentary spa access Monday-Sunday, 09:00-21:00.
- Access to fitness facilities Monday-Sunday.
- Complimentary yoga classes.
- 15% off standalone treatments.
- Exclusive member offers.

<p align="center">
  <img
    src="documentation/images/features/membership-page.png"
    alt="Repose annual membership page"
    width="700"
  >
</p>

The annual membership costs £999 and is paid in a single payment through Stripe Checkout.

Visitors who wish to purchase a membership must first create an account. If they are not registered, they are redirected to the registration page and then returned to the membership process to complete their purchase.

For active members, the purchase button is replaced with a link to their membership information under My Account.

### Booking Step One

The first booking step allows the user to choose between:

- Spa Access
- Treatment
- Package

When Treatment or Package is selected, JavaScript displays the corresponding service field while hiding the irrelevant field.
The available booking options depend on the user's membership status. For authenticated users with an active membership, the Spa Access option is removed, as complimentary spa access is already included in their membership. These users can still book treatments and packages, with a 15% discount applied to eligible standalone treatments.

<p align="center">
  <img
    src="documentation/images/features/booking-step-one.png"
    alt="First step of the Repose booking form"
    width="700"
  >
</p>

After successful validation, the booking type and related treatment or package ID are stored temporarily in the session and the user continues to the booking details step.

### Booking Details

The Booking Details page collects the booking date, time and guest quantity.

Available times depend on the selected booking type and service. Backend validation prevents users from selecting past dates or invalid same-day times.

<p align="center">
  <img
    src="documentation/images/features/booking-details.png"
    alt="Repose booking details form with date time and guest selection"
    width="700"
  >
</p>

The date field is enhanced so the date picker can be opened by clicking the field rather than only the browser calendar icon.

### Guest Details

Guest details are collected before the final review stage. Logged-in users can reuse account details, while guest users can enter the information required for the booking.

<p align="center">
  <img
    src="documentation/images/features/guest-details.png"
    alt="Repose guest details form"
    width="700"
  >
</p>

### Booking Review

The Booking Review page provides a final summary before payment, including the selected service, date, time, guest quantity and total price.

<p align="center">
  <img
    src="documentation/images/features/booking-review.png"
    alt="Repose booking review page before Stripe payment"
    width="700"
  >
</p>

For active members booking a standalone treatment, the 15% member discount is reflected in the review price. Packages remain at full price.

The user can cancel and return to the website or continue to Stripe Checkout.

### Stripe Checkout

Stripe Checkout is used for secure test-mode payments for both bookings and memberships.

<p align="center">
  <img
    src="documentation/images/features/stripe-checkout.png"
    alt="Stripe Checkout payment page for a Repose booking"
    width="700"
  >
</p>

Declined card payments are handled directly by Stripe's hosted checkout page, allowing the user to retry without leaving the payment flow.

### Payment Success and Cancellation

After successful payment, the user is returned to a confirmation page. The application also verifies the Stripe Checkout Session and updates the related booking or membership.

<p align="center">
  <img
    src="documentation/images/features/payment-success.png"
    alt="Repose payment success confirmation page"
    width="700"
  >
</p>

If the user cancels the Checkout flow, a cancellation page explains that the purchase was not completed.

### Registration Page

Visitors can create an account through the Registration page. Registration is used for personalised account features and is required before purchasing a membership.

<p align="center">
  <img
    src="documentation/images/features/register-page.png"
    alt="Repose registration form"
    width="700"
  >
</p>

The registration form validates account details on the backend and prevents duplicate email addresses.

### Login Page

Existing users can log in using their username and password.

<p align="center">
  <img
    src="documentation/images/features/login-page.png"
    alt="Repose login form"
    width="700"
  >
</p>

### My Account Page

The My Account page is available to authenticated users and provides a personal overview of bookings and membership status.

Upcoming and previous bookings are shown in separate sections using the same reusable card layout as the treatment and package pages.

<p align="center">
  <img
    src="documentation/images/features/account-page.png"
    alt="Repose My Account page showing bookings and membership information"
    width="700"
  >
</p>

If the user has an active membership, the membership start and end dates are displayed. Otherwise, a call to action links to the Membership page.

### Custom 404 Page

A custom 404 page is displayed when a user attempts to visit a route that does not exist. It uses the shared Repose layout and provides a clear link back to the Home page.

<p align="center">
  <img
    src="documentation/images/features/404-page.png"
    alt="Custom Repose 404 page with return to home button"
    width="700"
  >
</p>

### Django Admin

Django Admin provides authorised administrators with full CRUD functionality for the application's database records.

Administrators can:

- **Create** new treatments, packages, bookings and membership records.
- **Read** and review existing records and their related data.
- **Update** service details, prices, availability, bookings and memberships.
- **Delete** records that are no longer required.

This allows the site owner to manage the spa's services and operational data through the admin interface without editing the application code directly.

<p align="center">
  <img
    src="documentation/images/features/django-admin.png"
    alt="Django Admin interface for Repose Spa & Wellness"
    width="900"
  >
</p>

---

# Booking & Membership Development

## Multi-Step Booking Approach

The booking feature was developed in stages to keep the project structure clear and manageable. The first booking page was initially created as a simple interface to establish the intended flow before adding the full Django form and database logic.

The final process separates booking into multiple stages so users are not presented with one large form. This also allows validation to happen at the correct point in the journey.

## Session Handling

The first booking step captures the booking type and, where relevant, the selected Treatment or Package database ID.

After validation, only simple values are stored temporarily in the user's session rather than complete Django model objects. These values are then used to rebuild the booking information during later steps of the booking process.

This keeps the multi-step flow organised while avoiding premature database records before enough booking information has been collected.

## Member Spa Access Rule

Active Repose members receive complimentary spa access seven days a week as part of their annual membership.

When an authenticated user enters the booking process, the application checks their membership status. If the user has an active membership, Spa Access is excluded from the available booking options, since this service is already included in their membership.

This prevents members from unnecessarily purchasing spa access while keeping treatment and package bookings available.

## Membership Architecture

Membership is implemented as an optional upgrade to a normal user account rather than a separate authentication type.

A `Membership` record is connected to Django's existing `User` model through a `OneToOneField`. This keeps authentication simple while allowing membership-specific information and benefits to be linked directly to an account.

A membership stores its start date, end date and active status. After successful Stripe payment, the membership is created or updated for the authenticated user and remains active for 12 months.

## Member Treatment Booking Rule

The 15% standalone treatment discount is intended to be a personal membership benefit.

To prevent a member from using their discount for several guests in one treatment booking, an active member is limited to one guest when booking a standalone treatment. Non-members can book treatments for multiple guests at the standard price.

This rule is enforced in the backend booking logic rather than relying only on the displayed form choices.

## Package Guest Rules

Packages can define how many guests are included in one package through the `guests_per_package` field.

For example, Repose for Two represents one package for two guests. Valid booking quantities are therefore restricted to multiples of two: 2, 4 or 6 guests.

This prevents a two-person package from being incorrectly booked for a single guest and ensures pricing can be calculated using the correct number of package units.

## Stripe Checkout & Webhooks

Stripe Checkout is used for booking and membership payments in test mode.

When a booking payment begins:

1. The booking is saved with a `pending` payment status.
2. A Stripe Checkout Session is created.
3. The booking ID is passed through `client_reference_id` so Stripe events can be matched to the correct database record.
4. The user is redirected to Stripe Checkout.
5. After successful payment, the success view retrieves the Checkout Session and verifies that Stripe reports the payment as paid.
6. A Stripe webhook independently processes Checkout events so the database can still be updated even if the user closes the browser or does not return to the success page.

Webhook requests are verified using the Stripe signing secret stored in an environment variable.

The webhook listens for:

- `checkout.session.completed`
- `checkout.session.expired`

## Payment Status Flow

Booking payments use three states:

- `pending` - a booking has been created but payment has not yet been confirmed.
- `paid` - Stripe confirms that payment completed successfully.
- `cancelled` - the user cancels the flow or the Stripe Checkout Session expires while the booking is still pending.

A separate `failed` state was considered during development. It was removed because Stripe Checkout already handles card declines within the hosted checkout page and allows the user to retry immediately. Keeping a second Django failure flow would have duplicated Stripe's existing responsibility.

---

# Design & Accessibility

## Navigation

The main navigation provides access to Home, About Us, Treatments, Packages, Membership and Booking. Authentication-specific links change depending on whether the user is signed in.

On smaller screens, navigation is displayed through a hamburger menu. JavaScript toggles the menu state and updates `aria-expanded`, while CSS controls the animation and visual transition from the hamburger icon to a close icon.

## Layout

Repose uses:

- A shared Django base template with a consistent header and footer.
- Reusable treatment, package, account and Home page cards.
- Reusable form and button components.
- Responsive grid layouts.
- Clear content sections separated with subtle borders and spacing.
- A mobile-first responsive design.

### Colour Scheme

The Repose colour palette was selected to create a calm, understated and editorial spa aesthetic.

The main colours are stored as CSS custom properties:

```css
--color-background: #e8e7e7;
--color-text: #1a1a1a;
--color-primary: #ffffff;
--color-secondary: #333333;
--color-accent: #040495;
--color-highlight: #dfddd1;
```

<p align="center">
  <img
    src="documentation/images/features/color-palette.png"
    alt="Repose Spa & Wellness colour palette"
    width="900"
  >
</p>

### Typography

Repose uses two Google Fonts:

- **Cormorant Garamond** for the main interface and content.
- **Great Vibes** for the Repose brand wordmark.

Georgia and Times New Roman are used selectively for certain form controls and small metadata where browser rendering is clearer and more consistent.

### Responsive Design

Repose was developed using a mobile-first approach. Base styles are written for smaller screens and progressively enhanced through `min-width` media queries.

The main breakpoints currently used are:

```css
435px
700px
900px
1168px
1265px
```

These breakpoints were chosen based on where individual layouts required more space rather than forcing every component to use one universal breakpoint. For example, the full desktop navigation remains visible until the available space becomes too narrow, at which point it changes directly to the hamburger menu.

Responsive behaviour includes:

- Hamburger navigation on smaller screens.
- Single-column service and Home card layouts on mobile.
- Two-column card grids on larger screens.
- Responsive forms and action buttons.
- Footer layout changing from stacked content to a single row.
- Responsive hero imagery, typography and spacing.

Detailed responsive testing will be documented in [TESTING.md](TESTING.md).

### Accessibility

Accessibility considerations include:

- Semantic HTML elements and heading structure.
- Descriptive form labels.
- Backend validation in addition to browser-level constraints.
- Keyboard-accessible links and buttons.
- `:focus-visible` styles for interactive elements.
- `aria-label`, `aria-controls` and `aria-expanded` on the mobile navigation toggle.
- Alternative text for meaningful images.
- Reduced-motion support for the hero animation through `prefers-reduced-motion`.
- Clear colour contrast between text, controls and backgrounds.
- A custom 404 page that provides a clear route back to the website.

---

## User Stories

### Visitor User Stories

| User Story | Outcome |
| --- | --- |
| As a visitor, I want to understand what Repose offers so that I can decide whether the spa suits my needs. | The Home, About, Treatments, Packages and Membership pages explain the available services. |
| As a visitor, I want to browse treatments so that I can compare available options. | Treatments are grouped by category with descriptions, duration and price. |
| As a visitor, I want to browse spa packages so that I can choose a combined experience. | Package cards show descriptions, inclusions, duration and price. |
| As a visitor, I want to understand the membership benefits before joining. | The Membership page describes access, discounts and annual pricing. |
| As a visitor, I want to make a booking online so that I do not need to contact the spa manually. | A multi-step booking flow is available. |
| As a visitor, I want invalid choices to be prevented so that I can complete a valid booking. | Backend validation checks service selection, dates, times and guest rules. |
| As a visitor, I want to register so that I can access personalised features. | A Registration page is available. |
| As a visitor, I want the site to work on my device. | The website uses a mobile-first responsive layout. |

### Registered User Stories

| User Story | Outcome |
| --- | --- |
| As a registered user, I want to log in securely so that I can access my account information. | Django authentication provides login and logout functionality. |
| As a registered user, I want to view my upcoming bookings so that I can remember what I have reserved. | Confirmed future bookings appear under My Account. |
| As a registered user, I want to view previous bookings so that I have a simple booking history. | Previous booking dates appear in a separate account section. |
| As a registered user, I want to purchase a membership so that I can access member benefits. | Stripe Checkout activates a Membership record linked to the user. |
| As a registered user, I want to see whether my membership is active. | My Account displays membership status and validity dates. |

### Member User Stories

| User Story | Outcome |
| --- | --- |
| As a member, I want my treatment discount applied automatically so that I receive the correct price. | Eligible standalone treatments receive a 15% discount. |
| As a member, I want my benefit to remain personal to my membership. | Member treatment bookings are limited to one guest when the discount applies. |
| As a member, I want to access the spa without making a separate booking so that I can use my complimentary membership benefit. | Active members receive complimentary spa access seven days a week, and the Spa Access booking option is removed from their booking flow. |

### Administrator / Site Owner User Stories

| User Story | Outcome |
| --- | --- |
| As an administrator, I want to manage treatments so that service information remains accurate. | Treatment records can be managed in Django Admin. |
| As an administrator, I want to manage packages so that inclusions and pricing can be updated. | Package records can be managed in Django Admin. |
| As an administrator, I want to review bookings so that customer reservations can be managed. | Booking records are available in Django Admin. |
| As an administrator, I want to manage memberships so that active membership records can be reviewed. | Membership records are available in Django Admin. |
| As the site owner, I want payment status to update reliably so that paid and abandoned bookings are distinguishable. | Stripe webhooks update completed and expired Checkout Sessions. |

---

## Future Features & Improvements

Possible future improvements include:

- **Email-based login** - allow customers to sign in with their email address rather than Django's default username-based authentication.
- **Online booking management** - allow authenticated users to cancel or reschedule eligible bookings from My Account.
- **Back navigation within the booking flow** - allow users to return to earlier booking steps while preserving session data.
- **Booking confirmation emails** - send transactional confirmation emails after successful booking and membership payments.
- **Live availability and capacity management** - track how many places remain for each date and time slot and prevent overbooking.
- **Treatment or package preselection** - automatically preselect the relevant treatment or package when a user enters the booking flow through a service card, reducing the number of steps required.
- **Online membership payment plans** - allow users to choose between a one-time annual payment and supported instalment options.
- **Expanded member area** - provide additional membership history, offers and account management.
- **Real payment mode** - move Stripe from test mode to live mode if the project were used by a real business.
- **Automated booking reminders** - send reminders before upcoming appointments.
- **More detailed administrative availability controls** - allow staff to block specific dates or time slots.

---

## Entity Relationship Diagram

The Entity Relationship Diagram below was created using **Lucidchart** and provides a simplified overview of the relationships between the main models used in Repose Spa & Wellness.

<p align="center">
  <img
    src="documentation/images/features/repose-erd.png"
    alt="Entity relationship diagram for the Repose Spa & Wellness application"
    width="700"
  >
</p>

The main relationships shown in the diagram are:

- A **User** can have one **Membership**, which stores the membership status and validity period associated with that account.
- A **User** can have multiple **Bookings**, allowing registered users to keep a record of their confirmed reservations.
- A **Booking** can reference a **Treatment** when the selected booking type is a standalone treatment.
- A **Booking** can reference a **Package** when the selected booking type is a spa package.
- A **Spa Access** booking does not require a relationship with either a Treatment or Package, as the booking itself contains the information required for that booking type.

These relationships allow the application to use a shared Booking model for different types of reservations while keeping treatments, packages and memberships as separate database entities.

---

## Data Model

Repose uses a relational database together with Django's built-in `User` model.

### Treatment

The `Treatment` model stores standalone spa treatments.

| Field | Type | Purpose |
| --- | --- | --- |
| `name` | CharField | Treatment name |
| `description` | TextField | Treatment description |
| `category` | CharField | Massage, body treatment or facial category |
| `duration` | PositiveIntegerField | Treatment duration in minutes |
| `price` | DecimalField | Treatment price |
| `is_active` | BooleanField | Controls whether the treatment is available on the website |

### Package

The `Package` model stores combined spa experiences.

| Field | Type | Purpose |
| --- | --- | --- |
| `name` | CharField | Package name |
| `description` | TextField | Package description |
| `included` | TextField | Included items entered one per line |
| `price` | DecimalField | Package price |
| `guests_per_package` | PositiveIntegerField | Number of guests represented by one package |
| `duration` | PositiveIntegerField | Package duration in minutes |
| `time_period` | CharField | Used to control valid booking times |
| `is_active` | BooleanField | Controls whether the package is available |

The `included_items` property uses `splitlines()` to convert the stored text into a clean Python list for template display.

### Booking

The `Booking` model stores customer bookings and payment status.

Key information includes:

| Field | Purpose |
| --- | --- |
| User relationship | Links authenticated bookings to a user when available |
| Booking type | Identifies spa access, treatment or package |
| Treatment / Package relationship | Links the booking to the selected service where relevant |
| Guest information | Stores booking contact information |
| Booking date and time | Stores the selected reservation slot |
| Number of guests | Stores booking quantity |
| Payment status | Tracks pending, paid or cancelled payment state |
| Created timestamp | Records when the booking was created |

### Membership

The `Membership` model represents an annual Repose membership and is linked one-to-one with a user account.

| Field | Purpose |
| --- | --- |
| `user` | User who owns the membership |
| `start_date` | Membership activation date |
| `end_date` | Membership expiry date |
| `is_active` | Current active status |

---

## Technologies Used

### Languages

- **HTML5** - page structure and semantic content.
- **CSS3** - custom styling, responsive design, animations and layout.
- **JavaScript** - hamburger navigation, dynamic booking fields and date picker interaction.
- **Python** - server-side application logic and validation.

### Frameworks and Libraries

| Technology | Purpose |
| --- | --- |
| Django 4.2 | Full-stack web framework |
| Stripe | Hosted Checkout and payment webhooks |
| Gunicorn | Production web server |
| WhiteNoise | Static-file serving in production |
| dj-database-url | Production database configuration |
| psycopg2-binary | PostgreSQL database adapter |

### Database

| Environment | Database |
| --- | --- |
| Local development | SQLite |
| Production | PostgreSQL through Heroku Postgres |

### Tools

| Tool | Purpose |
| --- | --- |
| Git | Version control |
| GitHub | Repository hosting and deployment integration |
| Visual Studio Code | Development environment |
| Chrome Developer Tools | Debugging and responsive testing |
| Django Admin | Database administration |
| Heroku | Deployment and production hosting |
| Stripe Dashboard | Checkout and webhook configuration |
| Stripe CLI | Local webhook forwarding and payment testing |

---

## Testing

Detailed testing documentation is available in

[TESTING.md](TESTING.md)

Testing includes:

- Manual feature testing.
- User-story testing.
- Authentication testing.
- Booking validation testing.
- Membership functionality testing.
- Stripe Checkout and webhook testing.
- Responsive testing.
- Browser compatibility testing.
- Accessibility testing.
- HTML validation.
- CSS validation.
- JavaScript validation.
- Python linting.
- Lighthouse testing.

---

## Bugs

### Fixed Bugs

The following issues were identified and resolved during development.

| Bug | Cause | Solution |
| --- | --- | --- |
| Treatments appeared under the wrong category | The template initially looped through all treatments without separating them by category. | The view was updated to filter Massage, Body Treatments and Facials separately, with individual template loops. |
| Past booking dates could be selected | The booking date field initially had no minimum date and no backend rejection of past values. | Added a minimum date to the widget and backend `clean_booking_date()` validation. |
| Same-day time validation used the wrong local time | Validation relied on the project's previous timezone configuration. | Set the project timezone to `Europe/London` and used timezone-aware `localdate()` and `localtime()` checks. |
| Repose for Two could be selected for an invalid guest quantity | All packages originally shared the same 1-6 guest choices. | Added `guests_per_package` and generated valid guest choices in multiples of the package size. |
| Booking could continue without a selected treatment or package | Selecting a booking type did not guarantee that the corresponding service had been selected. | Added custom `BookingForm.clean()` validation requiring the relevant service. |
| Successful Stripe payment remained pending in Django | Stripe payment succeeded but the success flow did not initially update the related booking. | Added the Checkout Session ID to the success URL, retrieved the Stripe session and updated the booking after confirming `payment_status == "paid"`. |
| Abandoned Stripe payments remained pending indefinitely | A booking was created before Stripe Checkout and could remain pending when the user closed the payment page. | Added `checkout.session.expired` webhook handling to mark still-pending bookings as cancelled. |
| Stripe membership success raised an `AttributeError` | Stripe metadata was returned as a `StripeObject`, while the code attempted to use dictionary `.get()` access. | Converted Stripe metadata using `.to_dict()` and used Stripe-compatible access for other session values. |
| Missing `{% endif %}` in `membership.html` | A conditional block was not closed correctly. | Added the missing template closing tag and verified the page rendered correctly. |
| Heroku Django Admin returned a server error | Heroku initially deployed the project with Python 3.14.8, which caused compatibility problems in the project environment. | Added a root `.python-version` file specifying Python 3.12 and redeployed the application. |
| Booking review buttons became vertically misaligned on wider screens | `.review-payment` inherited bottom padding, making its flex-item box taller than the neighbouring Cancel link when the action container switched to a row. | Removed `.review-payment` from the shared bottom-padding rule so both actions align correctly. |
| 404 page appeared unstyled during local `DEBUG=False` testing | Local Django development server static-file behaviour differs when debug mode is disabled. | Verified the custom 404 page in the deployed Heroku environment where WhiteNoise serves static assets correctly. |

### Current Limitations

The following are intentional limitations rather than unresolved bugs:

- Stripe remains in test mode and does not process real money.
- Users cannot currently cancel or reschedule bookings through My Account.
- Booking availability does not yet track real spa capacity for individual time slots.
- Membership payment plans must be arranged directly with the spa rather than through the website.
- Yoga class booking is handled outside the current web application.
- The multi-step booking flow does not currently include a Back button between every stage.

---

## Deployment

Repose Spa & Wellness is deployed on Heroku and uses PostgreSQL in production.

The deployed application uses:

- **Heroku** for cloud hosting.
- **Heroku Postgres** for the production relational database.
- **Gunicorn** as the production web server.
- **WhiteNoise** for static-file serving.
- **Stripe** in test mode for payments.
- Environment variables for sensitive Django and Stripe configuration.

The deployed application can be viewed here:

- [Repose Spa & Wellness Live Site](https://repose-cff44b1bb103.herokuapp.com/)

### Version Control

Git was used throughout development, with GitHub used as the remote repository.

The project was developed through small, descriptive commits. The Heroku application is connected to the GitHub repository so updates to the deployment branch can be deployed automatically.

### Deployment Preparation

Production dependencies include:

```text
gunicorn
psycopg2-binary
dj-database-url
whitenoise
stripe
```

The exact installed versions are stored in `requirements.txt`.

A `Procfile` in the project root tells Heroku how to start the application:

```text
web: gunicorn config.wsgi
```

A `.python-version` file is used to define the supported Python runtime:

```text
3.12
```

### Environment Variables

Sensitive values are stored as Heroku Config Vars and are not committed to GitHub.

| Key | Purpose |
| --- | --- |
| `SECRET_KEY` | Django secret key |
| `DEBUG` | Controls Django debug mode; set to `False` in production |
| `DATABASE_URL` | Production PostgreSQL connection, provided through Heroku Postgres |
| `STRIPE_PUBLIC_KEY` | Stripe test publishable key |
| `STRIPE_SECRET_KEY` | Stripe test secret key |
| `STRIPE_WEBHOOK_SECRET` | Verifies incoming Stripe webhook requests |

### Static Files

WhiteNoise is used to serve static assets in production.

The WhiteNoise middleware is placed after Django's security middleware in `settings.py`, and a static root is configured so Django can collect production assets.

Static files are collected during deployment using Django's `collectstatic` process.

### Stripe Webhook Configuration

A Stripe webhook endpoint is configured for the deployed application at:

```text
/stripe/webhook/
```

The endpoint listens for:

```text
checkout.session.completed
checkout.session.expired
```

The deployed webhook signing secret is stored securely as a Heroku environment variable.

During local development, Stripe CLI can forward events to the local Django server for webhook testing.

### Heroku Deployment Steps

1. Create a new Heroku application.
2. Add Heroku Postgres to the application.
3. Add the required Config Vars in Heroku Settings.
4. Confirm the project contains `requirements.txt`, `Procfile` and `.python-version`.
5. Connect the Heroku application to the GitHub repository through the Deploy tab.
6. Select the `main` branch.
7. Enable automatic deployment or deploy the branch manually.
8. Run database migrations in the production environment.
9. Create a Django superuser for administration.
10. Load the initial services fixture into the production database.
11. Configure the production Stripe webhook and add its signing secret to Heroku.
12. Open the deployed application and test the booking, membership, static files, admin interface and payment flow.

The initial Repose service data is stored in a Django fixture:

```text
services/fixtures/services_data.json
```

The fixture can be loaded into a new environment with:

```bash
python manage.py loaddata services_data
```

> The fixture should only be loaded when required to avoid duplicate or conflicting initial records.

### Local Development

To run Repose locally, Python and Git must be installed.

#### Cloning

1. Open the Repose GitHub repository.
2. Select **Code** and copy the HTTPS, SSH or GitHub CLI URL.
3. Clone the repository:

   ```bash
   git clone https://github.com/Fannyhenriques/milestone-project-4.git
   ```

4. Enter the project directory:

   ```bash
   cd milestone-project-4
   ```

5. Create a virtual environment:

   ```bash
   python -m venv venv
   ```

6. Activate the virtual environment.

   macOS / Linux:

   ```bash
   source venv/bin/activate
   ```

   Windows:

   ```bash
   venv\Scripts\activate
   ```

7. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

8. Configure the required environment variables for local development.

9. Apply migrations:

   ```bash
   python manage.py migrate
   ```

10. Load the service fixture if required:

    ```bash
    python manage.py loaddata services_data
    ```

11. Create a superuser if administrator access is required:

    ```bash
    python manage.py createsuperuser
    ```

12. Start the development server:

    ```bash
    python manage.py runserver
    ```

13. Open:

    ```text
    http://127.0.0.1:8000/
    ```

The local project uses SQLite by default unless a different database connection is configured.

### Forking

To create an independent copy of the repository:

1. Log in to GitHub.
2. Open the Repose repository.
3. Select **Fork**.
4. Choose the account where the fork should be created.
5. GitHub creates an independent copy that can be modified without affecting the original repository.

---

## Credits

### Code and Documentation

- [Django 4.2 Documentation](https://docs.djangoproject.com/en/4.2/) - Reference for models, forms, views, authentication, sessions, validation, admin and timezone handling.
- [Stripe Documentation](https://docs.stripe.com/) - Reference for Checkout Sessions, test payments, metadata, webhooks and payment events.
- [Heroku Dev Center](https://devcenter.heroku.com/) - Reference for deployment, Config Vars, Python runtime configuration and Heroku Postgres.
- [WhiteNoise Documentation](https://whitenoise.readthedocs.io/) - Reference for production static file handling.
- [Gunicorn Documentation](https://gunicorn.org/) - Reference for production web server configuration.
- [dj-database-url](https://github.com/jazzband/dj-database-url) - Reference for configuring the production database from `DATABASE_URL`.
- [MDN Web Docs](https://developer.mozilla.org/) - Reference for HTML, CSS, JavaScript, responsive design and accessibility.
- [Stack Overflow - Making the HTML date input fully clickable](https://stackoverflow.com/questions/67967129/how-can-i-make-the-whole-html-date-field-clickable) - Reference for making the full calendar/date input clickable rather than only the browser calendar icon.
- Code Institute course material - Django structure, testing and deployment.

### Development and Testing Tools

- **Chrome Developer Tools / Inspector** - Used for debugging, responsive testing, layout inspection and checking browser behaviour.
- [W3C HTML Validator](https://validator.w3.org/) - HTML validation.
- [W3C CSS Validator](https://jigsaw.w3.org/css-validator/) - CSS validation.
- [JSHint](https://jshint.com/) - JavaScript validation and linting.
- **Python linter** - Python code quality and style checks.
- [Lighthouse](https://developer.chrome.com/docs/lighthouse/) - Performance, accessibility, best-practice and SEO testing.


