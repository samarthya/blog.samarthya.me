---
title: "Writing to a file in Linux deep-dive"
date: "2024-02-14T12:00:00Z"
slug: "writing-to-a-file-in-linux-deep-dive"
description: "Previously I gave a high level flow for how a process of simple file write looks like in a Linux environment here. In this blog, I will add more tech-details."
categories: ["technical"]
tags: ["linux"]
aliases: ["/wps/2024/02/14/writing-to-a-file-in-linux-deep-dive/"]
recovered: "Internet Archive snapshot 2026-03-13"
---

![](gem5.jpg)

Previously I gave a high level flow for how a process of simple file write looks like in a Linux environment [here]({{< relref "/posts/how-a-file-write-happens-in-linux" >}}). In this blog, I will add more tech-details. Let’s say I want to write “Hello World” to a file `/home/samarthya/myfile.txt` – What happens behind the scene?

We’ll assume the data resides on the first partition of a disk accessible as `/dev/sda1`.

**1. User application:**

- You issue a `write` system call with the path `/home/samarthya/myfile.txt` and data “Hello World”.

**2. Kernel space:**

- **System call handler:** Translates the path to a file descriptor.
- **VFS:**
  - Verifies your *permissions* to write to the file.
  - Locates the *inode* for the file based on the directory structure.
  - Identifies the file system type (e.g., ext4, NTFS) from the inode.
  - Uses the file system type to find the corresponding device driver.
- **Inode:**
  - Stores metadata about the file, including:
    - File size (currently 0 bytes).
    - Block information (where data will be written).
  - In this case, the block info might point to free blocks on the device.
- **Device driver:**
  - Receives the data (“Hello World”) and instructions (file descriptor, desired offset).
  - Calculates the target block addresses on the device using the offset and block information from the inode.
  - Prepares the data for writing, possibly performing buffering or padding to match the device’s requirements.
  - Communicates with the physical device:
    - Uses specific commands to write the data to the calculated block addresses.
    - Might involve DMA for faster transfers or direct register access.
  - Updates the inode:
    - Increases the file size to reflect the written data.
    - Might update block allocation information if new blocks were used.

**3. Response:**

- The system call returns successfully, indicating the write operation completed.
- The application might query the file size to confirm the write.

**Additional details:**

- **Kernel modules:** The device driver might be a kernel module loaded dynamically when needed.
- **Error handling:** Device drivers handle errors like full storage or communication failures and report them back to the user space.
- **Caching:** Some devices and file systems might use caching for better performance.
- **Concurrency:** Multiple processes attempting to write to the same file concurrently require synchronization mechanisms.

We talked about file path to descriptor translation, here are some details about that process

## Beyond the System Call: Path to File Descriptor Translation

While the basic path translates to a file descriptor through the system call handler, there’s more to the story under the hood!

Let’s dive deeper

### 1. System Call:

- You initiate a write operation, passing the path `/home/samarthya/myfile.txt`.
- The `write` system call handler intercepts the request. It doesn’t directly handle paths.

### 2. Userspace to Kernel Transition:

- The handler switches execution from user space to kernel space, entering the kernel’s memory protection.
- It translates the system call arguments into kernel structures, creating a `struct nameidata` object. This object holds the path string, current working directory, and flags for the operation.

### 3. VFS (Virtual File System):

- The VFS layer receives the `struct nameidata` from the system call handler.
- It doesn’t know specific file systems; it provides a unified interface for various filesystems.
- VFS starts navigating the path using the following steps:
  - **Parse and Split:** The path string is parsed into components (e.g., `/`, `home`, `samarthya`, etc.).
  - **Resolve Root**: `/` signifies the root directory. VFS identifies the root inode based on the currently mounted filesystem.
  - **Iterate Through Components:** For each remaining component in the path:
    - VFS calls the appropriate `lookup` function of the current filesystem type (e.g., ext4\_lookup for ext4 filesystem).
    - The `lookup` function searches the directory associated with the current inode for the specified component.
    - If found, it retrieves the corresponding inode for the component (e.g., the inode for `home` directory).
    - VFS updates the `struct nameidata` with the new inode and directory pointer.
    - This loop continues until the final component (myfile.txt) is reached.

### 4. Final Lookup and Inode Acquisition:

- After iterating through all components, VFS obtains the final inode representing the target file (`myfile.txt`).
- The `struct nameidata` now holds the complete path resolution and the associated inode.

### 5. File Descriptor Allocation:

- VFS calls the `open` function of the specific filesystem.
- The `open` function allocates a free file descriptor from the kernel’s file descriptor table.
- It associates the allocated file descriptor with the acquired inode in a file descriptor entry.
- This entry stores additional information like file access permissions, open flags, and pointers to internal data structures.

### 6. Return to User Space:

- VFS returns the allocated file descriptor to the system call handler.
- The handler switches back to user space and returns the file descriptor to your application.

**Additional Notes:**

- Error handling occurs at each step. Failure to find a component or insufficient permissions will result in errors returned to the application.
- Symbolic links are resolved during the lookup process, following their target paths until reaching a regular file.
- Caching mechanisms within VFS and filesystems can optimize repeated lookups.

This deeper explanation highlights the intricate work performed behind the scenes to translate a seemingly simple path into a file descriptor, showcasing the collaboration between system calls, VFS, and filesystem-specific routines.
