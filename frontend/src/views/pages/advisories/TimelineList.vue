<script>
import { AdvisoryTabMenu, AdvisoryTimelineCreateDialog } from '@/partials/advisories';
import { Stepper, StepperDescription, StepperItem, StepperSeparator, StepperTitle, StepperTrigger } from '@/components/ui/stepper';
import { CheckIcon, CircleIcon, DotIcon } from '@radix-icons/vue';
import { Button } from '@/components/ui/button';
import ContainerLayout from '@/layouts/ContainerLayout.vue';
import { Label } from '@/components/ui/label';
import { Input } from '@/components/ui/input';
import DatePicker from '@/components/datepicker/DatePicker.vue';
import BlankSlate from '@/components/blankslate/BlankSlate.vue';
import { Timeline } from '@/components/timeline';

export default {
    name: 'TimelineList',
    data() {
        return {
            advisoryId: this.$route.params.advisoryId,
            items: [],
            newModel: {
                date: null,
                text: null
            },
            showCreateForm: false
        };
    },
    mounted() {
        this.getItems();
    },
    methods: {
        getItems() {
            this.$api.get(this.$api.e.aTimelineList, { aPk: this.advisoryId }).then((response) => {
                this.items = response.data.results;
            });
        },
        save() {
            let data = {
                date: this.newModel.date,
                text: this.newModel.text
            };
            this.$api.post(this.$api.e.aTimelineList, { aPk: this.advisoryId }, data).then(() => {
                this.newModel = { date: null, text: null };
                this.getItems();
            });
        },
        confirmDialogDelete(id) {
            this.$confirm.require({
                message: 'Do you want to remove this item?',
                header: 'Delete confirmation',
                accept: () => {
                    this.$api.delete(this.$api.e.aTimelineDetail, { aPk: this.advisoryId, pk: id }).then(() => {
                        this.$toaster({
                            title: 'Deleted',
                            description: 'Item was removed!',
                            duration: 3000
                        });
                        this.getItems();
                    });
                }
            });
        }
    },
    components: {
        BlankSlate,
        Timeline,
        DatePicker,
        Label,
        ContainerLayout,
        AdvisoryTabMenu,
        AdvisoryTimelineCreateDialog,
        Stepper,
        StepperDescription,
        StepperItem,
        StepperSeparator,
        StepperTitle,
        StepperTrigger,
        CheckIcon,
        CircleIcon,
        DotIcon,
        Button,
        Input
    }
};
</script>

<template>
    <ContainerLayout>
        <template #left-header>
            <AdvisoryTabMenu></AdvisoryTabMenu>
        </template>
        <template #right-header>
            <Button
                @click="
                    () => {
                        this.showCreateForm = true;
                    }
                "
            >
                <i class="fa fa-plus"></i> Timeline Item
            </Button>
        </template>
        <Card class="col-span-12 mb-3" v-if="showCreateForm">
            <div class="flex flex-wrap md:flex-nowrap items-stretch gap-4 mt-3">
                <div class="flex flex-col w-full md:w-auto flex-grow gap-2">
                    <Label class="text-sm font-medium" for="date">Date</Label>
                    <DatePicker v-model="newModel.date"></DatePicker>
                </div>
                <div class="flex flex-col w-full md:w-auto flex-grow gap-2">
                    <Label class="text-sm font-medium" for="text">Text</Label>
                    <Input id="text" v-model="newModel.text"></Input>
                </div>
                <div class="flex gap-2 ml-auto flex-col md:flex-row items-end mt-4 md:mt-0">
                    <Button
                        variant="outline"
                        @click="
                            () => {
                                this.showCreateForm = false;
                            }
                        "
                        >Cancel
                    </Button>
                    <Button variant="default" @click="save">Save</Button>
                </div>
            </div>
        </Card>

        <Card class="flex justify-center">
            <div v-if="items.length > 0" class="mx-auto w-full max-w-2xl">
                <Timeline @delete="confirmDialogDelete" v-model:items="items" />
            </div>
            <BlankSlate v-else title="No Timeline Items!" text="No timeline items found!" icon="fa fa-timeline"></BlankSlate>
        </Card>
    </ContainerLayout>
</template>
