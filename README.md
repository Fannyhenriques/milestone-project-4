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


