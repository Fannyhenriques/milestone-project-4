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


