import { useParams } from "react-router-dom";
import { useState } from "react";
import { Link } from "react-router-dom";
import { useLocation } from "react-router-dom";

function Stock(props) {
  let { company } = useParams();
  const location = useLocation();
  const { stock } = location.state;

  const [sidebarVisible, setVisibileSidebar] = useState(false);

  function showSide(e) {
    setVisibileSidebar(!sidebarVisible);
    console.log(sidebarVisible);
  }
  function limitDescriptionToFourSentences(description) {
    const sentences = description.split(/\.+|\?+|!+/); // Split text into sentences based on periods, question marks, and exclamation marks.
    const firstFourSentences = sentences.slice(0, 6); // Get the first 4 sentences.
    return firstFourSentences.join(". ") + "."; // Join the sentences back together with periods and add a final period.
  }

  let arr = stock["titles"].split("}, {");
  let res = [];
  arr.forEach(function (line) {
    line = line.replace("title': '", "")
    .replace("', 'source'", " | Source:")
    .replace("[", "")
    .replace("{", "")
    .replace('"', "")
    .replace("youtube", "YouTube")
    .replace("reddit", "Reddit")
    .replace("news", "News")
    .replace("positive'", "Positive")
    .replace("negative'", "Negative")
    .replace("\", 'source': '", " | Source: ")
    .replace("'", "")
    .replace("}", "")
    .replace("]", "")
    .replace(":", "")
    .replace("', 'role': '", " | Sentiment: ")
    .replace("'", "")
    .replace("&#39;", "'")
    .replace("title ", "")
    .replace("Source::", "Source:");
    res.push(line);
  });

  return (
    <>
      <nav class="fixed z-30 w-full bg-white border-b border-gray-200 dark:bg-gray-800 dark:border-gray-700">
        <div class="px-3 py-3 lg:px-5 lg:pl-3">
          <div class="flex items-center justify-between">
            {/* menu bar and search */}
            <div class="flex items-center justify-start">
              <button
                onClick={showSide}
                id="toggleSidebarMobile"
                aria-expanded="true"
                aria-controls="sidebar"
                class="p-2 text-gray-600 rounded cursor-pointer hover:text-gray-900 hover:bg-gray-100 focus:bg-gray-100 dark:focus:bg-gray-700 focus:ring-2 focus:ring-gray-100 dark:focus:ring-gray-700 dark:text-gray-400 dark:hover:bg-gray-700 dark:hover:text-white"
              >
                <svg
                  id="toggleSidebarMobileHamburger"
                  class="w-6 h-6"
                  fill="currentColor"
                  viewBox="0 0 20 20"
                  xmlns="http://www.w3.org/2000/svg"
                >
                  <path
                    fill-rule="evenodd"
                    d="M3 5a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zM3 10a1 1 0 011-1h6a1 1 0 110 2H4a1 1 0 01-1-1zM3 15a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1z"
                    clip-rule="evenodd"
                  ></path>
                </svg>
              </button>
              <a href="" class="flex ml-2 md:mr-24">
                <Link to="/">
                  <span class="self-center text-xl font-semibold sm:text-2xl whitespace-nowrap dark:text-white pl-4">
                    InvestIQ
                  </span>
                </Link>
              </a>

              {/* TODO search */}
              <form action="/" method="GET" class="hidden lg:block lg:pl-3.5">
                <label for="topbar-search" class="sr-only">
                  Search
                </label>
                <div class="relative mt-1 lg:w-96">
                  <div class="absolute inset-y-0 left-0 flex items-center pl-1 pointer-events-none">
                    <svg
                      class="w-5 h-5 text-gray-500 dark:text-gray-400"
                      fill="currentColor"
                      viewBox="0 0 20 20"
                      xmlns="http://www.w3.org/2000/svg"
                    >
                      <path
                        fill-rule="evenodd"
                        d="M8 4a4 4 0 100 8 4 4 0 000-8zM2 8a6 6 0 1110.89 3.476l4.817 4.817a1 1 0 01-1.414 1.414l-4.816-4.816A6 6 0 012 8z"
                        clip-rule="evenodd"
                      ></path>
                    </svg>
                  </div>
                  <input
                    type="text"
                    name="stock"
                    id="topbar-search"
                    class="bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-500 focus:border-primary-500 block w-full pl-10 p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500"
                    placeholder="Search"
                  />
                </div>
              </form>
            </div>

            {/* right side */}
            <div class="flex items-center">
              {/* notifications */}
              <button
                type="button"
                data-dropdown-toggle="notification-dropdown"
                class="p-2 text-gray-500 rounded-lg hover:text-gray-900 hover:bg-gray-100 dark:text-gray-400 dark:hover:text-white dark:hover:bg-gray-700"
              >
                <span class="sr-only">View notifications</span>
                <svg
                  class="w-6 h-6"
                  fill="currentColor"
                  viewBox="0 0 20 20"
                  xmlns="http://www.w3.org/2000/svg"
                >
                  <path d="M10 2a6 6 0 00-6 6v3.586l-.707.707A1 1 0 004 14h12a1 1 0 00.707-1.707L16 11.586V8a6 6 0 00-6-6zM10 18a3 3 0 01-3-3h6a3 3 0 01-3 3z"></path>
                </svg>
              </button>
              <div
                class="z-20 z-50 hidden max-w-sm my-4 overflow-hidden text-base list-none bg-white divide-y divide-gray-100 rounded shadow-lg dark:divide-gray-600 dark:bg-gray-700"
                id="notification-dropdown"
              >
                <div class="block px-4 py-2 text-base font-medium text-center text-gray-700 bg-gray-50 dark:bg-gray-700 dark:text-gray-400">
                  Notifications
                </div>
                <div>
                  <a
                    href="#"
                    class="flex px-4 py-3 border-b hover:bg-gray-100 dark:hover:bg-gray-600 dark:border-gray-600"
                  >
                    <div class="flex-shrink-0">
                      <img
                        class="rounded-full w-11 h-11"
                        src="/images/users/bonnie-green.png"
                        alt="Jese image"
                      />
                      <div class="absolute flex items-center justify-center w-5 h-5 ml-6 -mt-5 border border-white rounded-full bg-primary-700 dark:border-gray-700">
                        <svg
                          class="w-3 h-3 text-white"
                          fill="currentColor"
                          viewBox="0 0 20 20"
                          xmlns="http://www.w3.org/2000/svg"
                        >
                          <path d="M8.707 7.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l2-2a1 1 0 00-1.414-1.414L11 7.586V3a1 1 0 10-2 0v4.586l-.293-.293z"></path>
                          <path d="M3 5a2 2 0 012-2h1a1 1 0 010 2H5v7h2l1 2h4l1-2h2V5h-1a1 1 0 110-2h1a2 2 0 012 2v10a2 2 0 01-2 2H5a2 2 0 01-2-2V5z"></path>
                        </svg>
                      </div>
                    </div>
                    <div class="w-full pl-3">
                      <div class="text-gray-500 font-normal text-sm mb-1.5 dark:text-gray-400">
                        New message from{" "}
                        <span class="font-semibold text-gray-900 dark:text-white">
                          Bonnie Green
                        </span>
                        : "Hey, what's up? All set for the presentation?"
                      </div>
                      <div class="text-xs font-medium text-primary-700 dark:text-primary-400">
                        a few moments ago
                      </div>
                    </div>
                  </a>
                  <a
                    href="#"
                    class="flex px-4 py-3 border-b hover:bg-gray-100 dark:hover:bg-gray-600 dark:border-gray-600"
                  >
                    <div class="flex-shrink-0">
                      <img
                        class="rounded-full w-11 h-11"
                        src="/images/users/jese-leos.png"
                        alt="Jese image"
                      />
                      <div class="absolute flex items-center justify-center w-5 h-5 ml-6 -mt-5 bg-gray-900 border border-white rounded-full dark:border-gray-700">
                        <svg
                          class="w-3 h-3 text-white"
                          fill="currentColor"
                          viewBox="0 0 20 20"
                          xmlns="http://www.w3.org/2000/svg"
                        >
                          <path d="M8 9a3 3 0 100-6 3 3 0 000 6zM8 11a6 6 0 016 6H2a6 6 0 016-6zM16 7a1 1 0 10-2 0v1h-1a1 1 0 100 2h1v1a1 1 0 102 0v-1h1a1 1 0 100-2h-1V7z"></path>
                        </svg>
                      </div>
                    </div>
                    <div class="w-full pl-3">
                      <div class="text-gray-500 font-normal text-sm mb-1.5 dark:text-gray-400">
                        <span class="font-semibold text-gray-900 dark:text-white">
                          Jese leos
                        </span>{" "}
                        and{" "}
                        <span class="font-medium text-gray-900 dark:text-white">
                          5 others
                        </span>{" "}
                        started following you.
                      </div>
                      <div class="text-xs font-medium text-primary-700 dark:text-primary-400">
                        10 minutes ago
                      </div>
                    </div>
                  </a>
                  <a
                    href="#"
                    class="flex px-4 py-3 border-b hover:bg-gray-100 dark:hover:bg-gray-600 dark:border-gray-600"
                  >
                    <div class="flex-shrink-0">
                      <img
                        class="rounded-full w-11 h-11"
                        src="/images/users/joseph-mcfall.png"
                        alt="Joseph image"
                      />
                      <div class="absolute flex items-center justify-center w-5 h-5 ml-6 -mt-5 bg-red-600 border border-white rounded-full dark:border-gray-700">
                        <svg
                          class="w-3 h-3 text-white"
                          fill="currentColor"
                          viewBox="0 0 20 20"
                          xmlns="http://www.w3.org/2000/svg"
                        >
                          <path
                            fill-rule="evenodd"
                            d="M3.172 5.172a4 4 0 015.656 0L10 6.343l1.172-1.171a4 4 0 115.656 5.656L10 17.657l-6.828-6.829a4 4 0 010-5.656z"
                            clip-rule="evenodd"
                          ></path>
                        </svg>
                      </div>
                    </div>
                    <div class="w-full pl-3">
                      <div class="text-gray-500 font-normal text-sm mb-1.5 dark:text-gray-400">
                        <span class="font-semibold text-gray-900 dark:text-white">
                          Joseph Mcfall
                        </span>{" "}
                        and{" "}
                        <span class="font-medium text-gray-900 dark:text-white">
                          141 others
                        </span>{" "}
                        love your story. See it and view more stories.
                      </div>
                      <div class="text-xs font-medium text-primary-700 dark:text-primary-400">
                        44 minutes ago
                      </div>
                    </div>
                  </a>
                  <a
                    href="#"
                    class="flex px-4 py-3 border-b hover:bg-gray-100 dark:hover:bg-gray-600 dark:border-gray-600"
                  >
                    <div class="flex-shrink-0">
                      <img
                        class="rounded-full w-11 h-11"
                        src="/images/users/leslie-livingston.png"
                        alt="Leslie image"
                      />
                      <div class="absolute flex items-center justify-center w-5 h-5 ml-6 -mt-5 bg-green-400 border border-white rounded-full dark:border-gray-700">
                        <svg
                          class="w-3 h-3 text-white"
                          fill="currentColor"
                          viewBox="0 0 20 20"
                          xmlns="http://www.w3.org/2000/svg"
                        >
                          <path
                            fill-rule="evenodd"
                            d="M18 13V5a2 2 0 00-2-2H4a2 2 0 00-2 2v8a2 2 0 002 2h3l3 3 3-3h3a2 2 0 002-2zM5 7a1 1 0 011-1h8a1 1 0 110 2H6a1 1 0 01-1-1zm1 3a1 1 0 100 2h3a1 1 0 100-2H6z"
                            clip-rule="evenodd"
                          ></path>
                        </svg>
                      </div>
                    </div>
                    <div class="w-full pl-3">
                      <div class="text-gray-500 font-normal text-sm mb-1.5 dark:text-gray-400">
                        <span class="font-semibold text-gray-900 dark:text-white">
                          Leslie Livingston
                        </span>{" "}
                        mentioned you in a comment:{" "}
                        <span class="font-medium text-primary-700 dark:text-primary-500">
                          @bonnie.green
                        </span>{" "}
                        what do you say?
                      </div>
                      <div class="text-xs font-medium text-primary-700 dark:text-primary-400">
                        1 hour ago
                      </div>
                    </div>
                  </a>
                  <a
                    href="#"
                    class="flex px-4 py-3 hover:bg-gray-100 dark:hover:bg-gray-600"
                  >
                    <div class="flex-shrink-0">
                      <img
                        class="rounded-full w-11 h-11"
                        src="/images/users/robert-brown.png"
                        alt="Robert image"
                      />
                      <div class="absolute flex items-center justify-center w-5 h-5 ml-6 -mt-5 bg-purple-500 border border-white rounded-full dark:border-gray-700">
                        <svg
                          class="w-3 h-3 text-white"
                          fill="currentColor"
                          viewBox="0 0 20 20"
                          xmlns="http://www.w3.org/2000/svg"
                        >
                          <path d="M2 6a2 2 0 012-2h6a2 2 0 012 2v8a2 2 0 01-2 2H4a2 2 0 01-2-2V6zM14.553 7.106A1 1 0 0014 8v4a1 1 0 00.553.894l2 1A1 1 0 0018 13V7a1 1 0 00-1.447-.894l-2 1z"></path>
                        </svg>
                      </div>
                    </div>
                    <div class="w-full pl-3">
                      <div class="text-gray-500 font-normal text-sm mb-1.5 dark:text-gray-400">
                        <span class="font-semibold text-gray-900 dark:text-white">
                          Robert Brown
                        </span>{" "}
                        posted a new video: Glassmorphism - learn how to
                        implement the new design trend.
                      </div>
                      <div class="text-xs font-medium text-primary-700 dark:text-primary-400">
                        3 hours ago
                      </div>
                    </div>
                  </a>
                </div>
                <a
                  href="#"
                  class="block py-2 text-base font-normal text-center text-gray-900 bg-gray-50 hover:bg-gray-100 dark:bg-gray-700 dark:text-white dark:hover:underline"
                >
                  <div class="inline-flex items-center ">
                    <svg
                      class="w-5 h-5 mr-2"
                      fill="currentColor"
                      viewBox="0 0 20 20"
                      xmlns="http://www.w3.org/2000/svg"
                    >
                      <path d="M10 12a2 2 0 100-4 2 2 0 000 4z"></path>
                      <path
                        fill-rule="evenodd"
                        d="M.458 10C1.732 5.943 5.522 3 10 3s8.268 2.943 9.542 7c-1.274 4.057-5.064 7-9.542 7S1.732 14.057.458 10zM14 10a4 4 0 11-8 0 4 4 0 018 0z"
                        clip-rule="evenodd"
                      ></path>
                    </svg>
                    View all
                  </div>
                </a>
              </div>

              {/* user profile */}
              <div class="flex items-center ml-3">
                <div>
                  <button
                    type="button"
                    class="flex text-sm bg-gray-800 rounded-full focus:ring-4 focus:ring-gray-300 dark:focus:ring-gray-600"
                    id="user-menu-button-2"
                    aria-expanded="false"
                    data-dropdown-toggle="dropdown-2"
                  >
                    <span class="sr-only">Open user menu</span>
                    <img
                      class="w-8 h-8 rounded-full"
                      src="https://flowbite.com/docs/images/people/profile-picture-5.jpg"
                      alt="user photo"
                    />
                  </button>
                </div>
                <div
                  class="z-50 hidden my-4 text-base list-none bg-white divide-y divide-gray-100 rounded shadow dark:bg-gray-700 dark:divide-gray-600"
                  id="dropdown-2"
                >
                  <div class="px-4 py-3" role="none">
                    <p
                      class="text-sm text-gray-900 dark:text-white"
                      role="none"
                    >
                      Daniel
                    </p>
                    <p
                      class="text-sm font-medium text-gray-900 truncate dark:text-gray-300"
                      role="none"
                    >
                      Radcliffe
                    </p>
                  </div>
                  <ul class="py-1" role="none">
                    <li>
                      <a
                        href="#"
                        class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 dark:text-gray-300 dark:hover:bg-gray-600 dark:hover:text-white"
                        role="menuitem"
                      >
                        Dashboard
                      </a>
                    </li>
                    <li>
                      <a
                        href="#"
                        class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 dark:text-gray-300 dark:hover:bg-gray-600 dark:hover:text-white"
                        role="menuitem"
                      >
                        Settings
                      </a>
                    </li>
                    <li>
                      <a
                        href="#"
                        class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 dark:text-gray-300 dark:hover:bg-gray-600 dark:hover:text-white"
                        role="menuitem"
                      >
                        Sign out
                      </a>
                    </li>
                  </ul>
                </div>
              </div>
            </div>
          </div>
        </div>
      </nav>

      <div class="flex pt-16 overflow-hidden bg-gray-50 dark:bg-gray-900">
        {/* sidebar */}
        {sidebarVisible && (
          <aside
            id="sidebar"
            class="fixed top-0 left-0 z-20 flex flex-col flex-shrink-0 hidden w-64 h-full pt-16 font-normal duration-75 lg:flex transition-width"
            aria-label="Sidebar"
          >
            <div class="relative flex flex-col flex-1 min-h-0 pt-0 bg-white border-r border-gray-200 dark:bg-gray-800 dark:border-gray-700">
              <div class="flex flex-col flex-1 pt-5 pb-4 overflow-y-auto">
                {/* sidemenu items */}
                <div class="flex-1 px-3 space-y-1 bg-white divide-y divide-gray-200 dark:bg-gray-800 dark:divide-gray-700">
                  <ul class="pb-2 space-y-2">
                    <li>
                      <a
                        href=""
                        class="flex items-center p-2 text-base text-gray-900 rounded-lg hover:bg-gray-100 group dark:text-gray-200 dark:hover:bg-gray-700"
                      >
                        <svg
                          class="w-6 h-6 text-gray-500 transition duration-75 group-hover:text-gray-900 dark:text-gray-400 dark:group-hover:text-white"
                          fill="currentColor"
                          viewBox="0 0 20 20"
                          xmlns="http://www.w3.org/2000/svg"
                        >
                          <path d="M2 10a8 8 0 018-8v8h8a8 8 0 11-16 0z"></path>
                          <path d="M12 2.252A8.014 8.014 0 0117.748 8H12V2.252z"></path>
                        </svg>
                        <Link to="/">
                          <span class="ml-3" sidebar-toggle-item>
                            Dashboard
                          </span>
                        </Link>
                      </a>
                    </li>

                    <li>
                      <a
                        href=""
                        class="flex items-center p-2 text-base text-gray-900 rounded-lg hover:bg-gray-100 group dark:text-gray-200 dark:hover:bg-gray-700"
                      >
                        <svg
                          class="w-6 h-6 text-gray-500 transition duration-75 group-hover:text-gray-900 dark:text-gray-400 dark:group-hover:text-white"
                          fill="currentColor"
                          viewBox="0 0 20 20"
                          xmlns="http://www.w3.org/2000/svg"
                          aria-hidden="true"
                        >
                          <path
                            clip-rule="evenodd"
                            fill-rule="evenodd"
                            d="M8.34 1.804A1 1 0 019.32 1h1.36a1 1 0 01.98.804l.295 1.473c.497.144.971.342 1.416.587l1.25-.834a1 1 0 011.262.125l.962.962a1 1 0 01.125 1.262l-.834 1.25c.245.445.443.919.587 1.416l1.473.294a1 1 0 01.804.98v1.361a1 1 0 01-.804.98l-1.473.295a6.95 6.95 0 01-.587 1.416l.834 1.25a1 1 0 01-.125 1.262l-.962.962a1 1 0 01-1.262.125l-1.25-.834a6.953 6.953 0 01-1.416.587l-.294 1.473a1 1 0 01-.98.804H9.32a1 1 0 01-.98-.804l-.295-1.473a6.957 6.957 0 01-1.416-.587l-1.25.834a1 1 0 01-1.262-.125l-.962-.962a1 1 0 01-.125-1.262l.834-1.25a6.957 6.957 0 01-.587-1.416l-1.473-.294A1 1 0 011 10.68V9.32a1 1 0 01.804-.98l1.473-.295c.144-.497.342-.971.587-1.416l-.834-1.25a1 1 0 01.125-1.262l.962-.962A1 1 0 015.38 3.03l1.25.834a6.957 6.957 0 011.416-.587l.294-1.473zM13 10a3 3 0 11-6 0 3 3 0 016 0z"
                          ></path>
                        </svg>
                        <Link to="/">
                          <span class="ml-3" sidebar-toggle-item>
                            Settings
                          </span>
                        </Link>
                      </a>
                    </li>
                  </ul>

                  <div class="pt-2 space-y-2">
                    <a
                      href="https://github.com/themesberg/flowbite-admin-dashboard/issues"
                      target="_blank"
                      class="flex items-center p-2 text-base text-gray-900 transition duration-75 rounded-lg hover:bg-gray-100 group dark:text-gray-200 dark:hover:bg-gray-700"
                    >
                      <svg
                        class="flex-shrink-0 w-6 h-6 text-gray-500 transition duration-75 group-hover:text-gray-900 dark:text-gray-400 dark:group-hover:text-white"
                        fill="currentColor"
                        viewBox="0 0 20 20"
                        xmlns="http://www.w3.org/2000/svg"
                      >
                        <path
                          fill-rule="evenodd"
                          d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-2 0c0 .993-.241 1.929-.668 2.754l-1.524-1.525a3.997 3.997 0 00.078-2.183l1.562-1.562C15.802 8.249 16 9.1 16 10zm-5.165 3.913l1.58 1.58A5.98 5.98 0 0110 16a5.976 5.976 0 01-2.516-.552l1.562-1.562a4.006 4.006 0 001.789.027zm-4.677-2.796a4.002 4.002 0 01-.041-2.08l-.08.08-1.53-1.533A5.98 5.98 0 004 10c0 .954.223 1.856.619 2.657l1.54-1.54zm1.088-6.45A5.974 5.974 0 0110 4c.954 0 1.856.223 2.657.619l-1.54 1.54a4.002 4.002 0 00-2.346.033L7.246 4.668zM12 10a2 2 0 11-4 0 2 2 0 014 0z"
                          clip-rule="evenodd"
                        ></path>
                      </svg>
                      <span class="ml-3" sidebar-toggle-item>
                        Support
                      </span>
                    </a>
                  </div>
                </div>
              </div>

              {/* sidebar bottom menu */}
              <div
                class="absolute bottom-0 left-0 justify-center hidden w-full p-4 space-x-4 bg-white lg:flex dark:bg-gray-800"
                sidebar-bottom-menu
              >
                <a
                  href="#"
                  class="inline-flex justify-center p-2 text-gray-500 rounded cursor-pointer hover:text-gray-900 hover:bg-gray-100 dark:hover:bg-gray-700 dark:hover:text-white"
                >
                  <svg
                    class="w-6 h-6"
                    fill="currentColor"
                    viewBox="0 0 20 20"
                    xmlns="http://www.w3.org/2000/svg"
                  >
                    <path d="M5 4a1 1 0 00-2 0v7.268a2 2 0 000 3.464V16a1 1 0 102 0v-1.268a2 2 0 000-3.464V4zM11 4a1 1 0 10-2 0v1.268a2 2 0 000 3.464V16a1 1 0 102 0V8.732a2 2 0 000-3.464V4zM16 3a1 1 0 011 1v7.268a2 2 0 010 3.464V16a1 1 0 11-2 0v-1.268a2 2 0 010-3.464V4a1 1 0 011-1z"></path>
                  </svg>
                </a>
                <a
                  href=""
                  data-tooltip-target="tooltip-settings"
                  class="inline-flex justify-center p-2 text-gray-500 rounded cursor-pointer hover:text-gray-900 hover:bg-gray-100 dark:hover:bg-gray-700 dark:hover:text-white"
                >
                  <svg
                    class="w-6 h-6"
                    fill="currentColor"
                    viewBox="0 0 20 20"
                    xmlns="http://www.w3.org/2000/svg"
                  >
                    <path
                      fill-rule="evenodd"
                      d="M11.49 3.17c-.38-1.56-2.6-1.56-2.98 0a1.532 1.532 0 01-2.286.948c-1.372-.836-2.942.734-2.106 2.106.54.886.061 2.042-.947 2.287-1.561.379-1.561 2.6 0 2.978a1.532 1.532 0 01.947 2.287c-.836 1.372.734 2.942 2.106 2.106a1.532 1.532 0 012.287.947c.379 1.561 2.6 1.561 2.978 0a1.533 1.533 0 012.287-.947c1.372.836 2.942-.734 2.106-2.106a1.533 1.533 0 01.947-2.287c1.561-.379 1.561-2.6 0-2.978a1.532 1.532 0 01-.947-2.287c.836-1.372-.734-2.942-2.106-2.106a1.532 1.532 0 01-2.287-.947zM10 13a3 3 0 100-6 3 3 0 000 6z"
                      clip-rule="evenodd"
                    ></path>
                  </svg>
                </a>
                <div
                  id="tooltip-settings"
                  role="tooltip"
                  class="absolute z-10 invisible inline-block px-3 py-2 text-sm font-medium text-white transition-opacity duration-300 bg-gray-900 rounded-lg shadow-sm opacity-0 tooltip dark:bg-gray-700"
                >
                  Settings page
                  <div class="tooltip-arrow" data-popper-arrow></div>
                </div>
              </div>
            </div>
          </aside>
        )}

        <div class="px-4 pt-6">
          <div class="grid gap-4 grid-cols-2">
            {/* todays top pick */}
            <div class="p-4 bg-white border border-gray-200 rounded-lg shadow-sm col-span-2 dark:border-gray-700 sm:p-6 dark:bg-gray-800">
              <div class="flex items-center justify-between mb-4">
                <div class="flex-shrink-0">
                  <span class="text-xl font-bold leading-none text-gray-900 sm:text-2xl dark:text-white">
                    {stock["ticker"]}
                  </span>
                  <h3 class="text-base font-light text-gray-500 dark:text-gray-400">
                    NASDAQ
                  </h3>
                </div>

                <div class="flex items-center justify-end flex-1 text-base font-medium text-green-500 dark:text-green-400">
                  <div class="flex-shrink-0 w-20 h-20">
                    <img
                      class="w-full h-full rounded-full"
                      src={stock["logo_url"]}
                      alt=""
                    />
                  </div>
                </div>
              </div>

              <div class="flex items-center justify-between mb-4">
                <div class="flex-shrink-0">
                  <span class="text-l font-bold leading-none text-gray-900 sm:text-xl dark:text-white">
                    Hottness: {stock["perception"]}
                  </span>
                </div>
              </div>
              <div class="flex items-center justify-between mb-4">
                <div class="flex-shrink-0">
                  <span class="text-l font-bold leading-none text-gray-900 sm:text-xl dark:text-white">
                    Popularity: {stock["popularity"]}
                  </span>
                </div>
              </div>
              <div class="flex items-center justify-between mb-4">
                <div class="flex-shrink-0">
                  <span class="text-l font-bold leading-none text-gray-900 sm:text-xl dark:text-white">
                    Overall: {stock["overall_rating"]}
                  </span>
                </div>

                <div class="flex items-center justify-end flex-1 text-base font-medium text-green-500 dark:text-green-400">
                  <div class="flex-shrink-0">
                    Recommendation: {stock["recommend"]}
                  </div>
                </div>
              </div>
            </div>

            {/* gpt */}
            <div class="p-4 bg-white border border-gray-200 rounded-lg shadow-sm col-span-1 dark:border-gray-700 sm:p-6 dark:bg-gray-800">
              <div class="flex items-center justify-between mb-4">
                <div class="flex-shrink-0">
                  <span class="text-xl font-bold leading-none text-gray-900 sm:text-2xl dark:text-white">
                    Current Stock Price
                  </span>
                </div>

                <div class="flex items-center justify-end flex-1 text-base text-2xl text-green-500 dark:text-green-400">
                  ${stock["current_price"]}&nbsp;&nbsp;/&nbsp;&nbsp;
                  {stock["growth"]}%
                  <svg
                    class="w-5 h-5"
                    fill="currentColor"
                    viewBox="0 0 20 20"
                    xmlns="http://www.w3.org/2000/svg"
                  >
                    <path
                      fill-rule="evenodd"
                      d="M5.293 7.707a1 1 0 010-1.414l4-4a1 1 0 011.414 0l4 4a1 1 0 01-1.414 1.414L11 5.414V17a1 1 0 11-2 0V5.414L6.707 7.707a1 1 0 01-1.414 0z"
                      clip-rule="evenodd"
                    ></path>
                  </svg>
                </div>
              </div>
              <div class="flex items-center justify-between mb-4">
                <div class="flex-shrink-0">
                  <span class="text-xl font-bold leading-none text-gray-900 sm:text-2xl dark:text-white">
                    Current Market Cap
                  </span>
                </div>

                <div class="flex items-center justify-end flex-1 text-base text-2xl text-green-500 dark:text-green-400">
                  ${stock["market_cap"].toLocaleString()}
                  <svg
                    class="w-5 h-5"
                    fill="currentColor"
                    viewBox="0 0 20 20"
                    xmlns="http://www.w3.org/2000/svg"
                  >
                    <path
                      fill-rule="evenodd"
                      d="M5.293 7.707a1 1 0 010-1.414l4-4a1 1 0 011.414 0l4 4a1 1 0 01-1.414 1.414L11 5.414V17a1 1 0 11-2 0V5.414L6.707 7.707a1 1 0 01-1.414 0z"
                      clip-rule="evenodd"
                    ></path>
                  </svg>
                </div>
              </div>
              {/* Grey horizontal line */}
              <hr class="my-4 border-gray-200 dark:border-gray-600" />

              <div class="flex-shrink-0">
                <span class="text-xl font-bold leading-none text-gray-900 sm:text-2xl dark:text-white">
                  Market Analysis
                </span>
              </div>
              <br></br>
              <p class="text-white">{stock["blurb"]}</p>
            </div>

            {/* data */}
            <div class="p-4 bg-white border border-gray-200 rounded-lg shadow-sm col-span-1 dark:border-gray-700 sm:p-6 dark:bg-gray-800">
              <div class="flex items-center justify-between mb-4">
                <div class="flex-shrink-0">
                  <span class="text-xl font-bold leading-none text-gray-900 sm:text-2xl dark:text-white">
                    Description
                  </span>
                </div>
              </div>

              <p class="text-white">
                {limitDescriptionToFourSentences(stock["description"])}
              </p>
            </div>

            {/* data */}
            <div class="p-4 bg-white border border-gray-200 rounded-lg shadow-sm col-span-1 dark:border-gray-700 sm:p-6 dark:bg-gray-800">
              <div class="flex items-center justify-between mb-4">
                <div class="flex-shrink-0">
                  <span class="text-xl font-bold leading-none text-gray-900 sm:text-2xl dark:text-white">
                    Similar Investments
                  </span>
                </div>
              </div>

              <ul class="max-w-md space-y-1 text-gray-500 list-disc list-inside dark:text-gray-400">
                <li>LMT</li>
                <li>GD</li>
                <li>GE</li>
                <li>HON</li>
                <li>NOC</li>
              </ul>

              {/* <p class='text-white'>{Array.from(stock['similar']).map(d => d)}</p> */}
            </div>

            {/* data */}
            <div class="p-4 bg-white border border-gray-200 rounded-lg shadow-sm col-span-1 dark:border-gray-700 sm:p-6 dark:bg-gray-800">
              <div class="flex items-center justify-between mb-4">
                <div class="flex-shrink-0">
                  <span class="text-xl font-bold leading-none text-gray-900 sm:text-2xl dark:text-white">
                    Online Sentiments
                  </span>
                </div>
              </div>
              <dl class="max-w-md text-gray-900 divide-y divide-gray-200 dark:text-white dark:divide-gray-700">
                {res.map(function (data) {
                  return (
                    <div class="flex flex-col pb-3">
                      {/* <dt class="mb-1 text-green-500 md:text-lg ">Youtube - Positive</dt> */}
                      <dd class="text-lg font-semibold">{data}</dd>
                    </div>
                  );
                })}
              </dl>

              {/* <dl class="max-w-md text-gray-900 divide-y divide-gray-200 dark:text-white dark:divide-gray-700">
    <div class="flex flex-col pb-3">
        <dt class="mb-1 text-green-500 md:text-lg ">Youtube - Positive</dt>
        <dd class="text-lg font-semibold">Boeing Bear OUTRAGED By $400 Price Target</dd>
    </div>
    <div class="flex flex-col py-3">
        <dt class="mb-1 text-green-500 md:text-lg ">Youtube - Positive</dt>
        <dd class="text-lg font-semibold">Why BlackRock is BULLISH on Boeing Stock</dd>
    </div>
    <div class="flex flex-col pt-3">
        <dt class="mb-1 text-red-500 md:text-lg ">Reddit - Negative</dt>
        <dd class="text-lg font-semibold">Why Investors Keep Shorting Boeing More Than Any Other Stock</dd>
    </div>
</dl>    */}

              {/* <p class='text-white'>{Array.from(stock['titles']).map(d => d)}</p> */}
            </div>
          </div>

          <div class="grid my-4 grid-cols-2 grid-rows-4 gap-4">
            <div class="p-4 mb-4 bg-white border border-gray-200 rounded-lg shadow-sm dark:border-gray-700 sm:p-6 dark:bg-gray-800 xl:mb-0">
              <div class="absolute w-3 h-3 bg-gray-200 rounded-full mt-1.5 -left-1.5 border border-white dark:border-gray-800 dark:bg-gray-700"></div>
              <time class="mb-1 text-sm font-normal leading-none text-gray-400 dark:text-gray-500">
                Help
              </time>
              <h3 class="text-lg font-semibold text-gray-900 dark:text-white">
                Confused?
              </h3>
              <p class="text-base font-normal text-gray-500 dark:text-gray-400">
                Investing can be a hard game to figure out. For tips and tricks,
                feel free to look online, search videos on YouTube, and download
                a trading app and figure out the basics of how everything works.
                Use InvestIQ as a tool to inform your trading decisions.
              </p>
            </div>
          </div>
        </div>
      </div>
    </>
  );
}

export default Stock;
