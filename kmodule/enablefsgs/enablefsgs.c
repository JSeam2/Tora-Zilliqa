#include <linux/module.h>
#include <linux/init.h>
#include <linux/proc_fs.h>
#include <linux/slab.h>
#include <linux/errno.h>
#include <linux/string.h>
#include <linux/uaccess.h>
#include <linux/smp.h>
#include <asm/uaccess.h>
#include <asm/tlbflush.h>

MODULE_LICENSE("GPL");

static int __init module_oninit(void);
static void __exit module_onexit(void);
ssize_t proc_read_enablefsgs(struct file *file, char __user *buf, size_t size, loff_t *offset);

module_init(module_oninit);
module_exit(module_onexit);

struct file_operations proc_ops = {
    .owner = THIS_MODULE,
    .read = proc_read_enablefsgs
};

int read = 0;

static int __init module_oninit(void)
{
    if (!proc_create("enablefsgs", 0444, NULL, &proc_ops)) {
        printk(KERN_ERR "enablefsgs: failed to register proc entry\n");
        return -EINVAL;
    }

    printk(KERN_INFO "enablefsgs: successfully loaded\n");
    return 0;
}

static void __exit module_onexit(void)
{
    remove_proc_entry("enablefsgs", NULL);
    printk(KERN_INFO "enablefsgs: successfully unloaded\n");
}

void enable_fsgsbase(void *buf)
{
    uint64_t cr4;
    char *tmp_buf;

    /* Enable FSGSBASE on CR4 */
    cr4_set_bits(1 << 16); // Use kernel function instead of direct writing.
    asm volatile("mov %%cr4, %%rax\nmov %%rax, %0" : "=m" (cr4) :: "ax");

    tmp_buf = kmalloc(80, GFP_KERNEL);

    if (!tmp_buf) {
        printk(KERN_ERR "enablefsgs: failed to allocate buffer\n");
        return;
    }

    sprintf(tmp_buf, "FSGSBASE enabled on cpu %u, cr4 = %llx\n", smp_processor_id(), cr4);
    strcat((char *)buf, tmp_buf);

    kfree(tmp_buf);
}

ssize_t proc_read_enablefsgs(struct file *file, char __user *buf, size_t size, loff_t *offset)
{
    int len;
    char *out_buf;

    if (read) {
        read = 0;
        return 0;
    }
    read = 1;

    out_buf = kmalloc(80 * num_online_cpus(), GFP_KERNEL);

    if (!out_buf) {
        printk(KERN_ERR "enablefsgs: failed to allocate buffer\n");
        return -1;
    }

    strcpy(out_buf, "");
    on_each_cpu(enable_fsgsbase, out_buf, 1);

    len = strlen(out_buf);
    copy_to_user(buf, out_buf, len);

    kfree(out_buf);

    return (ssize_t)len;
}
